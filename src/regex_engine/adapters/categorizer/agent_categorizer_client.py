import asyncio

import openai
from agents import Agent, Runner, trace

from regex_engine.application.dto.agent.categorized_ingredient import CategorizedIngredient
from regex_engine.domain.enums import Category
from regex_engine.domain.errors import InvalidModelError

categorizer_prompt = """
Jesteś agentem klasyfikującym produkty spożywcze.
Na podstawie nazwy produktu przypisz go do DOKŁADNIE JEDNEJ kategorii z listy Category.

WORKFLOW:
1. Określ co to za produkt, napisz jego krótki, jednozdaniowy opis dla kontekstu.
2. Korzystając z opisu, który stworzyłeś dopasuj produkt do odpowiedniej kategorii. 
    Jeśli produkt pasuje do kilku kategorii, wybierz kategorię
    najbardziej wąską i najbardziej opisującą produkt
    (np.: rosół → zupy/buliony, a nie gotowe dania)
3. Napisz powód, który uzasadnia dokładnie tę wybraną kategorię.
4. Zwróć WYŁĄCZNIE poprawny JSON:
{{
  "category": "<wartość Category>",
  "name": "<oryginalna nazwa produktu>",
  "description": "<krótki opis produktu>",
  "reason": "<krótki powód (jedno zwięzłe zdanie, dlaczego ta kategoria)>"
}}
5. Jeśli jego opis jest zbyt krótki/niejasny/może definiować wiele składników umieść go w kategorii OTHER oraz napisz dlaczego tam trafił.

Reguły:
- Klasyfikuj wg dominującego charakteru produktu.
- Słodziki (miód, cukier, syropy, ksylitol, erytrytol) → SUGARS_AND_SWEETENERS.
- Kakao (proszek, nibsy, masa) → NUTS_AND_SEEDS, nigdy GRAINS.
- Kategoria "gotowe dania" używaj głównie dla gotowych dań/wyrobów wieloskładnikowych 
  (np. pierogi, pizza, dania gotowe, konserwy z dodatkami).
- Kategorie "przetworzone" używaj dla produktów, które wymagają przygotowania ale jednocześnie nie są osobnym daniem 
  (np. pesto, pasta tahini, masło orzechowe, kopytka, dżem)
  klasyfikuj do kategorii SUROWCA BAZOWEGO, a nie do "przetworzone".
- Zboża (ryż, mąka, kasze, pieczywo, makaron) → GRAINS.
- W razie istotnej niepewności → OTHER.
- Zero komentarzy poza JSON.

Dozwolone wartości pola "category" (DOKŁADNIE jedna z poniższych, bez zmian):
{category_enum_to_prompt()}

Przykłady:

Input: "miód wielokwiatowy"
Output:
{{
  "category": "cukry i słodziki",
  "name": "miód wielokwiatowy",
  "description": "Naturalny produkt pszczeli o słodkim smaku.",
  "reason": "Produkt pełni funkcję naturalnego słodzika."
}}

Input: "kakao naturalne 100% proszek"
Output:
{{
  "category": "orzechy i nasiona",
  "name": "kakao naturalne 100% proszek",
  "description": "Proszek otrzymany z ziaren kakaowca.",
  "reason": "Jest to produkt pochodzący z nasion kakaowca."
}}

Input: "ryż basmati"
Output:
{{
  "category": "produkty zbożowe",
  "name": "ryż basmati",
  "description": "Długoziarnisty ryż aromatyczny.",
  "reason": "Ryż jest produktem zbożowym."
}}

Input: "filet z łososia"
Output:
{{
  "category": "ryby i owoce morza",
  "name": "filet z łososia",
  "description": "Surowy filet z ryby morskiej.",
  "reason": "Łosoś jest rybą przeznaczoną do spożycia."
}}

Input: "jogurt naturalny"
Output:
{{
  "category": "nabiał",
  "name": "jogurt naturalny",
  "description": "Fermentowany produkt mleczny bez dodatków.",
  "reason": "Jest to produkt wytwarzany z mleka."
}}

Input: "mix śniadaniowy"
Output:
{{
  "category": "inne",
  "name": "mix śniadaniowy",
  "description": "Produkt o ogólnej nazwie bez precyzyjnego składu.",
  "reason": "Nazwa nie pozwala na jednoznaczną klasyfikację."
}}
"""


def category_enum_to_prompt() -> str:
    return "\n".join(f'- "{c.value}"' for c in Category)


def _build_categorizer_agent(model: str) -> Agent:
    return Agent(
        name="categorizer",
        instructions=categorizer_prompt,
        model=model,
        output_type=CategorizedIngredient,
    )


class AgentCategorizerClient:
    def __init__(self, model: str, timeout: int):
        self._agent = _build_categorizer_agent(model)
        self._timeout = timeout

    @classmethod
    async def create(cls, model: str, timeout: int) -> "AgentCategorizerClient":
        self = cls(model, timeout)
        await self._ping(model)
        return self

    async def categorize(self, ingredient: str, instance: int) -> CategorizedIngredient:
        with trace(f"Categorizer: {ingredient}, instance: {instance}"):
            result = await asyncio.wait_for(
                Runner.run(self._agent, ingredient),
                timeout=self._timeout,
            )
        return result.final_output

    async def _ping(self, model: str):
        try:
            await asyncio.wait_for(
                Runner.run(self._agent, "ping"),
                timeout=self._timeout,
            )
        except openai.BadRequestError as exc:
            raise InvalidModelError(f"Model `{model}` is invalid or unavailable") from exc
        except openai.AuthenticationError as exc:
            raise InvalidModelError("Invalid api key") from exc

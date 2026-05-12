from enum import Enum, auto


class EnsureIngredientStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"


class EnsureWordStatus(Enum):
    ALREADY_MATCHED = auto()
    UPDATED_EXISTING = auto()
    CREATED_NEW = auto()
    SKIPPED_EMPTY = auto()
    FAILED = auto()


class RegexKind(str, Enum):
    UNIT_SIZE = "unit_size"
    UNIT = "unit"
    INGREDIENT_CONDITION = "condition"
    INGREDIENT_NAME = "name"
    OR_CONJUNCTIONS = "or_conjunctions"
    AND_CONJUNCTIONS = "and_conjunctions"


class Category(str, Enum):
    DAIRY = "nabiał"
    MEAT = "mięso"
    FISH_AND_SEAFOOD = "ryby i owoce morza"
    EGGS = "jajka"
    GRAINS = "produkty zbożowe"
    VEGETABLES = "warzywa"
    FRUITS = "owoce"
    LEGUMES = "rośliny strączkowe"
    NUTS_AND_SEEDS = "orzechy i nasiona"
    FATS_AND_OILS = "tłuszcze i oleje"
    SUGARS_AND_SWEETENERS = "cukry i słodziki"
    SPICES_AND_HERBS = "przyprawy i zioła"
    SAUCES_AND_DRESSINGS = "sosy i dressingi"
    MUSHROOMS = "grzyby"
    PROCESSED = "przetworzone"
    PREPARED_MEALS = "gotowe dania"
    SOUPS = "zupy/buliony"
    BEVERAGES = "napoje"
    ALCOHOL = "alkohol"
    NON_FOOD = "niejadalne"
    OTHER = "inne"
    UNKNOWN = "nieznane"

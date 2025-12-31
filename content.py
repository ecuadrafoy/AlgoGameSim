from enum import Enum
from typing import Optional
import uuid


class CulturalEnum(Enum):
    """Enumeration for cultural attributes"""
    WESTERN = "western"
    EASTERN = "eastern"
    AFRICAN = "african"
    INDIGENOUS = "indigenous"
    MULTICULTURAL = "multicultural"


class Content:
    """
    Content class representing content/information in the simulation.
    Similar to Agent but allows all attributes to be optional/null.
    
    Attributes:
        content_id: Unique identifier for the content
        education: Education level (1-5) or None
        economic_status: Economic status (10,000-500,000, rounded to 5,000) or None
        ethics: Ethical values (0-1) or None
        politics: Political orientation (-2 to +2) or None
        cultural: Cultural background (enum) or None
        age: Age in years (5-90) or None
        sex: Biological sex (0 or 1) or None
        novelty: Preference for novelty (0-1) or None
        conscientiousness: Conscientiousness trait (0-1) or None
        impulsivity: Impulsivity trait (0-1) or None
        tech_affinity: Technology affinity (0-1) or None
        social_trust: Trust in social institutions (0-1) or None
    """
    
    def __init__(
        self,
        content_id: Optional[str] = None,
        education: Optional[int] = None,
        economic_status: Optional[float] = None,
        ethics: Optional[float] = None,
        politics: Optional[int] = None,
        cultural: Optional[CulturalEnum] = None,
        age: Optional[int] = None,
        sex: Optional[int] = None,
        novelty: Optional[float] = None,
        conscientiousness: Optional[float] = None,
        impulsivity: Optional[float] = None,
        tech_affinity: Optional[float] = None,
        social_trust: Optional[float] = None
    ):
        """
        Initialize Content with specified attributes (all optional).
        
        Args:
            content_id: Unique identifier (auto-generated if None)
            education: Education level (1-5) or None
            economic_status: Economic status value (10,000-500,000) or None
            ethics: Ethics value (0-1) or None
            politics: Political orientation (-2 to +2) or None
            cultural: Cultural background or None
            age: Age in years (5-90) or None
            sex: Biological sex (0 or 1) or None
            novelty: Novelty preference (0-1) or None
            conscientiousness: Conscientiousness level (0-1) or None
            impulsivity: Impulsivity level (0-1) or None
            tech_affinity: Technology affinity (0-1) or None
            social_trust: Social trust level (0-1) or None
            
        Raises:
            ValueError: If any attribute is outside its valid range (when not None)
        """
        self.content_id = content_id or str(uuid.uuid4())
        
        # Validate and set attributes (all allow None)
        self.education = self._validate_education(education) if education is not None else None
        self.economic_status = self._validate_economic_status(economic_status) if economic_status is not None else None
        self.ethics = self._validate_range(ethics, 0, 1, "ethics") if ethics is not None else None
        self.politics = self._validate_politics(politics) if politics is not None else None
        self.cultural = cultural if cultural is None or isinstance(cultural, CulturalEnum) else CulturalEnum(cultural)
        self.age = self._validate_age(age) if age is not None else None
        self.sex = self._validate_sex(sex) if sex is not None else None
        self.novelty = self._validate_range(novelty, 0, 1, "novelty") if novelty is not None else None
        self.conscientiousness = self._validate_range(conscientiousness, 0, 1, "conscientiousness") if conscientiousness is not None else None
        self.impulsivity = self._validate_range(impulsivity, 0, 1, "impulsivity") if impulsivity is not None else None
        self.tech_affinity = self._validate_range(tech_affinity, 0, 1, "tech_affinity") if tech_affinity is not None else None
        self.social_trust = self._validate_range(social_trust, 0, 1, "social_trust") if social_trust is not None else None
    
    @staticmethod
    def _validate_range(value: float, min_val: float, max_val: float, name: str) -> Optional[float]:
        """Validate that a value is within the specified range."""
        if value is None:
            return None
        if not (min_val <= value <= max_val):
            raise ValueError(f"{name} must be between {min_val} and {max_val}, got {value}")
        return value
    
    @staticmethod
    def _validate_education(value: Optional[int]) -> Optional[int]:
        """Validate education level (1-5)."""
        if value is None:
            return None
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError(f"education must be an integer between 1 and 5, got {value}")
        return value
    
    @staticmethod
    def _validate_economic_status(value: Optional[float]) -> Optional[float]:
        """Validate and round economic status to nearest 5,000 (range: 10,000-500,000)."""
        if value is None:
            return None
        if not isinstance(value, (int, float)):
            raise ValueError(f"economic_status must be a number, got {type(value)}")
        if not (10000 <= value <= 500000):
            raise ValueError(f"economic_status must be between 10,000 and 500,000, got {value}")
        # Round to nearest 5,000
        rounded_value = round(value / 5000) * 5000
        return rounded_value
    
    @staticmethod
    def _validate_politics(value: Optional[int]) -> Optional[int]:
        """Validate politics value (-2 to +2)."""
        if value is None:
            return None
        if not isinstance(value, int) or not (-2 <= value <= 2):
            raise ValueError(f"politics must be an integer between -2 and 2, got {value}")
        return value
    
    @staticmethod
    def _validate_age(value: Optional[int]) -> Optional[int]:
        """Validate age (5-90)."""
        if value is None:
            return None
        if not isinstance(value, int) or not (5 <= value <= 90):
            raise ValueError(f"age must be an integer between 5 and 90, got {value}")
        return value
    
    @staticmethod
    def _validate_sex(value: Optional[int]) -> Optional[int]:
        """Validate sex (0 or 1)."""
        if value is None:
            return None
        if value not in (0, 1):
            raise ValueError(f"sex must be 0 or 1, got {value}")
        return value
    
    def __repr__(self) -> str:
        """Return string representation of the content."""
        return (
            f"Content(id={self.content_id}, education={self.education}, "
            f"economic_status={self.economic_status}, ethics={self.ethics}, "
            f"politics={self.politics}, cultural={self.cultural.value if self.cultural else None}, "
            f"age={self.age}, sex={self.sex})"
        )
    
    def to_dict(self) -> dict:
        """Convert content attributes to a dictionary."""
        return {
            'content_id': self.content_id,
            'education': self.education,
            'economic_status': self.economic_status,
            'ethics': self.ethics,
            'politics': self.politics,
            'cultural': self.cultural.value if self.cultural else None,
            'age': self.age,
            'sex': self.sex,
            'novelty': self.novelty,
            'conscientiousness': self.conscientiousness,
            'impulsivity': self.impulsivity,
            'tech_affinity': self.tech_affinity,
            'social_trust': self.social_trust
        }

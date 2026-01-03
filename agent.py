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


class Agent:
    """
    Agent class representing an individual in the simulation.
    
    Attributes:
        agent_id: Unique identifier for the agent
        education: Education level (1-5)
        economic_status: Economic status (float)
        ethics: Ethical values (0-1)
        politics: Political orientation (-2 to +2)
        cultural: Cultural background (enum)
        age: Age in years (5-90)
        sex: Biological sex (0, 1, or 2)
        novelty: Preference for novelty (0-1)
        conscientiousness: Conscientiousness trait (0-1)
        impulsivity: Impulsivity trait (0-1)
        tech_affinity: Technology affinity (0-1)
        social_trust: Trust in social institutions (0-1)
    """
    
    def __init__(
        self,
        agent_id: Optional[str] = None,
        education: int = 1,
        economic_status: float = 0.5,
        ethics: float = 0.5,
        politics: int = 0,
        cultural: CulturalEnum = CulturalEnum.WESTERN,
        age: int = 30,
        sex: int = 0,
        novelty: float = 0.5,
        conscientiousness: float = 0.5,
        impulsivity: float = 0.5,
        tech_affinity: float = 0.5,
        social_trust: float = 0.5
    ):
        """
        Initialize an Agent with specified attributes.
        
        Args:
            agent_id: Unique identifier (auto-generated if None)
            education: Education level (1-5)
            economic_status: Economic status value
            ethics: Ethics value (0-1)
            politics: Political orientation (-2 to +2)
            cultural: Cultural background
            age: Age in years (5-90)
            sex: Biological sex (0, 1, or 2)
            novelty: Novelty preference (0-1)
            conscientiousness: Conscientiousness level (0-1)
            impulsivity: Impulsivity level (0-1)
            tech_affinity: Technology affinity (0-1)
            social_trust: Social trust level (0-1)
            
        Raises:
            ValueError: If any attribute is outside its valid range
        """
        self.agent_id = agent_id or str(uuid.uuid4())
        
        # Validate and set attributes
        self.education = self._validate_education(education)
        self.economic_status = self._validate_economic_status(economic_status)
        self.ethics = self._validate_range(ethics, 0, 1, "ethics")
        self.politics = self._validate_politics(politics)
        self.cultural = cultural if isinstance(cultural, CulturalEnum) else CulturalEnum(cultural)
        self.age = self._validate_age(age)
        self.sex = self._validate_sex(sex)
        self.novelty = self._validate_range(novelty, 0, 1, "novelty")
        self.conscientiousness = self._validate_range(conscientiousness, 0, 1, "conscientiousness")
        self.impulsivity = self._validate_range(impulsivity, 0, 1, "impulsivity")
        self.tech_affinity = self._validate_range(tech_affinity, 0, 1, "tech_affinity")
        self.social_trust = self._validate_range(social_trust, 0, 1, "social_trust")
    
    @staticmethod
    def _validate_range(value: float, min_val: float, max_val: float, name: str) -> float:
        """Validate that a value is within the specified range."""
        if not (min_val <= value <= max_val):
            raise ValueError(f"{name} must be between {min_val} and {max_val}, got {value}")
        return value
    
    @staticmethod
    def _validate_education(value: int) -> int:
        """Validate education level (1-5)."""
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError(f"education must be an integer between 1 and 5, got {value}")
        return value
    
    @staticmethod
    def _validate_economic_status(value: float) -> float:
        """Validate and round economic status to nearest 5,000 (range: 10,000-500,000)."""
        if not isinstance(value, (int, float)):
            raise ValueError(f"economic_status must be a number, got {type(value)}")
        if not (10000 <= value <= 500000):
            raise ValueError(f"economic_status must be between 10,000 and 500,000, got {value}")
        # Round to nearest 5,000
        rounded_value = round(value / 5000) * 5000
        return rounded_value
    
    @staticmethod
    def _validate_politics(value: int) -> int:
        """Validate politics value (-2 to +2)."""
        if not isinstance(value, int) or not (-2 <= value <= 2):
            raise ValueError(f"politics must be an integer between -2 and 2, got {value}")
        return value
    
    @staticmethod
    def _validate_age(value: int) -> int:
        """Validate age (5-90)."""
        if not isinstance(value, int) or not (5 <= value <= 90):
            raise ValueError(f"age must be an integer between 5 and 90, got {value}")
        return value
    
    @staticmethod
    def _validate_sex(value: int) -> int:
        """Validate sex (0, 1, or 2)."""
        if value not in (0, 1, 2):
            raise ValueError(f"sex must be 0, 1, or 2, got {value}")
        return value
    
    def __repr__(self) -> str:
        """Return string representation of the agent."""
        return (
            f"Agent(id={self.agent_id}, education={self.education}, "
            f"economic_status={self.economic_status}, ethics={self.ethics}, "
            f"politics={self.politics}, cultural={self.cultural.value}, age={self.age}, "
            f"sex={self.sex})"
        )
    
    def to_dict(self) -> dict:
        """Convert agent attributes to a dictionary."""
        return {
            'agent_id': self.agent_id,
            'education': self.education,
            'economic_status': self.economic_status,
            'ethics': self.ethics,
            'politics': self.politics,
            'cultural': self.cultural.value,
            'age': self.age,
            'sex': self.sex,
            'novelty': self.novelty,
            'conscientiousness': self.conscientiousness,
            'impulsivity': self.impulsivity,
            'tech_affinity': self.tech_affinity,
            'social_trust': self.social_trust
        }

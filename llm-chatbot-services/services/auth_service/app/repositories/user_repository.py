"""Repository for user data access"""
from typing import List, Dict, Optional

class UserRepository:
    """Repository for user data access"""
    def __init__(self):
        """Initialize the user repository"""
        # Simulate a user database
        self._users: List[Dict] = []

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get a user by email"""
        return next((u for u in self._users if u["email"] == email), None)

    def add_user(self, user_data: Dict) -> None:
        """Add a user to the repository"""
        self._users.append(user_data)

    def all_users(self) -> List[Dict]:
        """Get all users"""
        return self._users 
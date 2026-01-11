"""
Authentication Controller
Handles user authentication (Process 1.0 in DFD Level 1)
- Receives: Login Credentials from Admin, Librarian, Member
- Validates: Against User Database (Data Store 2.0)
- Returns: Login Status to respective users
"""

from datetime import datetime, timedelta
import hashlib
import json


class AuthenticationController:
    """
    Manages authentication operations including login and logout.
    Maps to Process 1.0 (Authentication) in DFD Level 1
    """

    def __init__(self):
        """Initialize authentication controller"""
        self.user_model = None
        self.active_sessions = {}  # Track active user sessions

    def set_user_model(self, user_model):
        """
        Set the user model for database operations
        
        Args:
            user_model: User model instance for accessing User Database
        """
        self.user_model = user_model

    def login(self, username: str, password: str) -> dict:
        """
        Process: 1.0 Authentication - Login
        Input: Login Credentials (username, password)
        Output: Login Status (success/failure with user info)
        
        Args:
            username (str): User's username
            password (str): User's password
            
        Returns:
            dict: Login status {
                'status': 'success'|'failure',
                'message': str,
                'user_id': int or None,
                'user_type': 'Admin'|'Librarian'|'Member' or None,
                'session_token': str or None
            }
        """
        # Validate input
        if not username or not password:
            return {
                'status': 'failure',
                'message': 'Username and password are required',
                'user_id': None,
                'user_type': None,
                'session_token': None
            }

        # Query User Database (Data Store: User Database)
        if not self.user_model:
            return {
                'status': 'failure',
                'message': 'User database not configured',
                'user_id': None,
                'user_type': None,
                'session_token': None
            }

        # Retrieve user from database
        user = self.user_model.get_user_by_username(username)

        if not user:
            return {
                'status': 'failure',
                'message': 'Invalid username or password',
                'user_id': None,
                'user_type': None,
                'session_token': None
            }

        # Verify password
        if not self._verify_password(password, user.get('password_hash')):
            return {
                'status': 'failure',
                'message': 'Invalid username or password',
                'user_id': None,
                'user_type': None,
                'session_token': None
            }

        # Check if user account is active
        if user.get('status') != 'active':
            return {
                'status': 'failure',
                'message': 'User account is inactive',
                'user_id': None,
                'user_type': None,
                'session_token': None
            }

        # Generate session token
        session_token = self._generate_session_token(user.get('user_id'))
        
        # Store active session
        self.active_sessions[session_token] = {
            'user_id': user.get('user_id'),
            'username': username,
            'user_type': user.get('user_type'),
            'login_time': datetime.now(),
            'last_activity': datetime.now()
        }

        # Return Login Status (Data Flow to users)
        return {
            'status': 'success',
            'message': f'Login successful for {user.get("user_type")}',
            'user_id': user.get('user_id'),
            'user_type': user.get('user_type'),
            'session_token': session_token
        }

    def logout(self, session_token: str) -> dict:
        """
        Process: 1.0 Authentication - Logout
        Input: Session Token
        Output: Logout Status
        
        Args:
            session_token (str): Active session token
            
        Returns:
            dict: Logout status {
                'status': 'success'|'failure',
                'message': str
            }
        """
        if session_token in self.active_sessions:
            del self.active_sessions[session_token]
            return {
                'status': 'success',
                'message': 'Logout successful'
            }
        
        return {
            'status': 'failure',
            'message': 'Invalid session token'
        }

    def verify_session(self, session_token: str) -> dict:
        """
        Verify if session token is valid and not expired
        
        Args:
            session_token (str): Session token to verify
            
        Returns:
            dict: Verification result {
                'is_valid': bool,
                'user_id': int or None,
                'user_type': str or None,
                'message': str
            }
        """
        if session_token not in self.active_sessions:
            return {
                'is_valid': False,
                'user_id': None,
                'user_type': None,
                'message': 'Invalid or expired session'
            }

        session = self.active_sessions[session_token]
        
        # Check session expiration (30 minutes timeout)
        if (datetime.now() - session['last_activity']) > timedelta(minutes=30):
            del self.active_sessions[session_token]
            return {
                'is_valid': False,
                'user_id': None,
                'user_type': None,
                'message': 'Session expired'
            }

        # Update last activity
        session['last_activity'] = datetime.now()

        return {
            'is_valid': True,
            'user_id': session['user_id'],
            'user_type': session['user_type'],
            'message': 'Session is valid'
        }

    def get_user_by_session(self, session_token: str) -> dict:
        """
        Get user information from session token
        
        Args:
            session_token (str): Active session token
            
        Returns:
            dict: User information or None if invalid
        """
        if session_token in self.active_sessions:
            session = self.active_sessions[session_token]
            return {
                'user_id': session['user_id'],
                'username': session['username'],
                'user_type': session['user_type']
            }
        
        return None

    def _hash_password(self, password: str) -> str:
        """
        Hash password using SHA-256
        
        Args:
            password (str): Plain text password
            
        Returns:
            str: Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify password against hash
        
        Args:
            password (str): Plain text password
            password_hash (str): Hashed password from database
            
        Returns:
            bool: True if password matches
        """
        return self._hash_password(password) == password_hash

    def _generate_session_token(self, user_id: int) -> str:
        """
        Generate unique session token
        
        Args:
            user_id (int): User ID
            
        Returns:
            str: Session token
        """
        token_data = f"{user_id}_{datetime.now().timestamp()}"
        return hashlib.sha256(token_data.encode()).hexdigest()

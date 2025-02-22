class UserRequest:
    """Represents a request received by the application to find a midpoint activity for a group of users."""
    
    def __init__(
        self,
        user_id: str,
        user_locations: list[tuple[float, float]], #changed from two user locations to a list so we can handle groups of users 
        activity_type: str,
        rating: float,
        price_category: float,
        time_needed: float,
    ):
        self.user_id = user_id
        self.user_locations = user_locations  #a list of user locations (latitude, longitude tuples) for all usrs in the group
        self.activity_type = activity_type
        self.rating = rating
        self.price_category = price_category
        self.time_needed = time_needed

    def __repr__(self):
        return f"UserRequest({self.user_id})"

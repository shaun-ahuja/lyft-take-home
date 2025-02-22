from activity import Activity
from metro_graph import MetroGraph, Station
from eta_calculator import ETACalculator
from user_request import UserRequest

class Suggestion():
    """A suggestion is an activity recommended based on a given user request."""
    def __init__(self, activity: Activity, user1_eta: float, user2_eta: float):
        self.activity = activity
        self.user1_eta = user1_eta
        self.user2_eta = user2_eta

    def print_details(self):
        print(f"Suggested activity: {self.activity.name}")
        print(f"Distance from User 1: {self.user1_eta} minutes")
        print(f"Distance from User 2: {self.user2_eta} minutes")


def suggest_midpoint_activity(
    user_locations: list[tuple[float, float]],  #changed to a list of user locations for group support
    activities: list[Activity],
    eta_calculator: ETACalculator,
    user_request: UserRequest #added user_request parameter for accessing request details like activity type, rating, etc.
) -> Suggestion:

    """
    Suggests a midpoint activity for a group of users based on commute time and fairness.
    Prioritizes activities that balance commute times and are close to the users' preferences.
    """
    #filter the activities based on user's preferences
    filtered_activities = [
        activity for activity in activities
        if activity.activity_type == user_request.activity_type
        and activity.rating >= user_request.rating
        and activity.price_category <= user_request.price_category
        and activity.time_needed <= user_request.time_needed
    ]
    
    #if there are no activities that meet the full criteria, then only filter by type of activity
    if not filtered_activities:
        filtered_activities = [
            activity for activity in activities
            if activity.activity_type == user_request.activity_type
        ]
    
    #if there are still no activities that much, return None
    if not filtered_activities:
        return None

    best_activity = None
    best_total_commute = float("inf")
    best_fairness_score = float("inf")

    #calculate the ETA for each of the activities, and then choose the best one based on total commute time and fairness
    for activity in filtered_activities:
        total_commute_time = 0
        max_commute_time = 0
        min_commute_time = float("inf")

        #calculate ETA for each of the users in the groups
        for location in user_locations:
            eta = eta_calculator.calculate_eta(location, activity.coordinates)
            total_commute_time += eta
            max_commute_time = max(max_commute_time, eta)
            min_commute_time = min(min_commute_time, eta)

        #find the fairness score as the difference between the max and min of the commute times 
        fairness_score = max_commute_time - min_commute_time

        #choose the activity with the best combination of minimal total commute time and fairness
        if total_commute_time < best_total_commute or (total_commute_time == best_total_commute and fairness_score < best_fairness_score):
            best_activity = activity
            best_total_commute = total_commute_time
            best_fairness_score = fairness_score

    #finally, return the best activity as a suggestion
    if best_activity:
        #only return ETA for the first two users (assuming pairwise comparison as the original code)
        user1_eta = eta_calculator.calculate_eta(user_locations[0], best_activity.coordinates)
        user2_eta = eta_calculator.calculate_eta(user_locations[1], best_activity.coordinates)
        return Suggestion(best_activity, user1_eta, user2_eta)

    return None

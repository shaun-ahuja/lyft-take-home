from eta_calculator import ETACalculator
from suggestion import suggest_midpoint_activity
#updated import statement to reflect updated name (load_user_grou_requests instead of load_user_requests)
from midpoint_utils import load_metro_graph, load_user_group_requests, load_activities


class Runner:
    def run(self):
        eta_calculator = ETACalculator(load_metro_graph())
        user_requests = load_user_group_requests()  #loaded group requests instead of pair requests
        activities = load_activities()

        print("Finding suggested activities...\n")

        for request in user_requests:
        #updated to handle user requests with multple user locations
            suggestion = suggest_midpoint_activity(
                request.user_locations,
                activities,
                eta_calculator,
                request)
            if suggestion is None:
                print(f"No suggestion generated for user group: {request.user_id}")
            else:
                print(f"Suggested activity for user group: {request.user_id}")
                suggestion.print_details()
            print()


if __name__ == "__main__":
    Runner().run()

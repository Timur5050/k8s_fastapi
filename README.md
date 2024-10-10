## API Implementation
1. /user/:username/url/*address
I developed an API endpoint that allows users to request a web address (*address). The server downloads the HTTP response from the provided address and returns the time taken in milliseconds. I also track the following per user:

    Total number of requests made by the user.
    Number of successful requests.
    Number of failed requests.
    Cumulative time spent on successful/failed requests.

2. /user/:username/stats
This endpoint returns user-specific statistics, such as:
    The total number of successful and failed requests.
    The average request time for both successful and failed requests.

3. /stats
An endpoint that aggregates and returns statistics across all users, ignoring the username dimension:
    Total number of successful and failed requests.
    Average request time for both successful and failed requests.

## Rate Limiting

To ensure fairness and prevent excessive usage, I implemented a configurable rate limiter that allows X requests per minute. This was configured per user and applies individually per instance of the web server. I also integrated rate-limiting statistics into the user stats, logging the number of requests that were throttled (i.e., rejected due to exceeding the rate limit).

## Kubernetes Deployment (Minikube)

I deployed the project on a Kubernetes cluster using Minikube for local development. Here’s a summary of the deployment:
    Helm Chart:
        Created a Helm chart for the web server.
        Configured the chart for high availability by ensuring at least two instances of the web server are running simultaneously. This makes each instance responsible for its own rate-limiting, ensuring no cross-instance interference.
    Port Forwarding:
        I set up port forwarding from the Minikube service to my local machine, making the service's APIs accessible. The forwarding is done at the service level (not the pod level) to ensure all instances can handle requests.
    Service Scaling:
        I verified the high availability setup by scaling the web server to two instances and confirming that each instance properly enforced its own rate limit while serving requests.

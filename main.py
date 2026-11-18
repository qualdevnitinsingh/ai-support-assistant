
import logging

from pydantic import ValidationError
from google.genai._gaos.lib import compat_errors

from analyzer import (analyze_customer_message, count_prompt_tokens)

# 1. Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(levelname)s: %(message)s"
)


# 2. Gemini 3.8 Flash Standard paid-tier pricing
# Rates are USD per 1 million tokens.
# These rates apply through December 31, 2026.

MODEL_PRICING = {
    "input": 0.75,
    "cached_input": 0.075,
    "output": 3.75
}


# 3. Extract token usage from Gemini response
def extract_usage_metrics(usage):

    if usage is None:
        return None

    return {
        "input_tokens": int(
            getattr(usage, "total_input_tokens", 0) or 0
        ),

        "output_tokens": int(
            getattr(usage, "total_output_tokens", 0) or 0
        ),

        "thought_tokens": int(
            getattr(usage, "total_thought_tokens", 0) or 0
        ),

        "cached_tokens": int(
            getattr(usage, "total_cached_tokens", 0) or 0
        ),

        "total_tokens": int(
            getattr(usage, "total_tokens", 0) or 0
        ),

        "tool_use_tokens": int(
            getattr(usage, "total_tool_use_tokens", 0) or 0
        )
    }


# 4. Estimate standard paid-tier request cost
def estimate_paid_tier_cost(metrics):

    input_tokens = metrics["input_tokens"]
    cached_tokens = min(
        metrics["cached_tokens"],
        input_tokens
    )

    uncached_tokens = input_tokens - cached_tokens

    # Calculate uncached input cost
    input_cost = (
        uncached_tokens *
        MODEL_PRICING["input"] / 1_000_000
    )

    # Calculate cached input cost
    cached_cost = (
        cached_tokens *
        MODEL_PRICING["cached_input"] / 1_000_000
    )

    # Google charges thinking tokens at output rates
    billable_output_tokens = (
        metrics["output_tokens"] +
        metrics["thought_tokens"]
    )

    output_cost = (
        billable_output_tokens *
        MODEL_PRICING["output"] / 1_000_000
    )

    return input_cost + cached_cost + output_cost


# 5. Display usage for one request
def display_request_usage(metrics):

    if metrics is None:

        print("\nToken usage metadata is unavailable.")
        return

    estimated_cost = estimate_paid_tier_cost(metrics)

    metrics["estimated_paid_tier_cost"] = estimated_cost

    print("\n" + "-" * 50)
    print("TOKEN USAGE - THIS REQUEST")
    print("-" * 50)

    print(f"Input tokens: {metrics['input_tokens']:,}")
    print(f"Output tokens: {metrics['output_tokens']:,}")
    print(f"Thinking tokens: {metrics['thought_tokens']:,}")
    print(f"Cached input tokens: {metrics['cached_tokens']:,}")
    print(f"Tool-use tokens: {metrics['tool_use_tokens']:,}")
    print(f"Total tokens: {metrics['total_tokens']:,}")

    print(
        "Estimated paid-tier cost: "
        f"${estimated_cost:.8f} USD"
    )


# 6. Process one customer message
def process_customer_message(message, previous_interaction_id):

    try:

        try:

            prompt_tokens = count_prompt_tokens(message)

            print("\nPRE-REQUEST TOKEN COUNT")
            print("System instructions + customer message:", prompt_tokens)

        except Exception:

            logging.exception("Unable to count tokens before request")

            print("Token pre-count unavailable. Continuing with AI request.")

        analysis, new_interaction_id, usage = (
            analyze_customer_message(
                message,
                previous_interaction_id=previous_interaction_id
            )
        )

        # Display AI analysis
        print("\n" + "-" * 50)
        print("AI CUSTOMER SUPPORT ANALYSIS")
        print("-" * 50)

        print("Category:", analysis.category)
        print("Priority:", analysis.priority)
        print("Sentiment:", analysis.sentiment)

        print("\nSummary:")
        print(analysis.summary)

        print("\nRequired Action:")
        print(analysis.required_action)

        print("\nSuggested Customer Reply:")
        print(analysis.suggested_reply)

        print("-" * 50)

        # Extract and display usage
        metrics = extract_usage_metrics(usage)
        display_request_usage(metrics)

        return new_interaction_id, metrics

    except ValidationError as exc:

        print("\nERROR: AI response validation failed.")
        print(exc)

    except ValueError as exc:

        print("\nERROR: Invalid input or response.")
        print(exc)

    except compat_errors.APIError as exc:

        status_code = getattr(exc, "status_code", None)
        details = getattr(exc, "body", None) or str(exc)

        print("\nERROR: Gemini API request failed.")
        print("HTTP Status:", status_code)
        print("Details:", details)

        error_details = str(details).lower()

        if status_code in (400, 401) and (
            "api key" in error_details
            or "credential" in error_details
        ):
            print("Check your Gemini API key.")

        elif status_code == 400:
            print("Check the API request parameters.")

        elif status_code == 401:
            print("Authentication failed.")

        elif status_code == 403:
            print("Access denied. Check API permissions.")

        elif status_code == 404:
            print("Requested model or resource not found.")

        elif status_code == 429:
            print("API rate limit or quota exceeded.")

        elif status_code is not None and status_code >= 500:
            print("Gemini service may be temporarily unavailable.")

    except Exception:

        logging.exception("Unexpected error during message analysis")

        print("\nERROR: An unexpected application error occurred.")
        print("Please check application logs.")

    # Preserve the previous ID if the request failed
    return previous_interaction_id, None


# 7. Display cumulative usage
def display_session_usage(totals):

    print("\n" + "=" * 50)
    print("CUMULATIVE SESSION USAGE")
    print("=" * 50)

    print(f"Input tokens: {totals['input_tokens']:,}")
    print(f"Output tokens: {totals['output_tokens']:,}")
    print(f"Thinking tokens: {totals['thought_tokens']:,}")
    print(f"Cached tokens: {totals['cached_tokens']:,}")
    print(f"Total tokens: {totals['total_tokens']:,}")

    print(
        "Estimated paid-tier cost: "
        f"${totals['estimated_cost']:.8f} USD"
    )


# 8. Interactive application
def main():

    previous_interaction_id = None

    # Track usage across this application session
    session_totals = {
        "input_tokens": 0,
        "output_tokens": 0,
        "thought_tokens": 0,
        "cached_tokens": 0,
        "total_tokens": 0,
        "estimated_cost": 0.0
    }

    print("\n" + "=" * 50)
    print("AI CUSTOMER SUPPORT ASSISTANT")
    print("=" * 50)

    print("\nEnter a customer message to analyze.")
    print("Type '/new' to start a fresh conversation.")
    print("Type 'exit' or 'quit' to close the application.")

    while True:

        try:

            message = input("\nCustomer Message: ").strip()

            if message.lower() in ("exit", "quit"):

                print("\nClosing AI Customer Support Assistant.")

                display_session_usage(session_totals)

                break

            if message.lower() == "/new":

                previous_interaction_id = None

                print("\nStarted a new conversation.")
                continue

            if not message:

                print("Please enter a customer message.")
                continue

            print("\nAnalyzing customer message...")

            previous_interaction_id, metrics = (
                process_customer_message(
                    message,
                    previous_interaction_id
                )
            )

            # Update cumulative totals after successful requests
            if metrics is not None:

                session_totals["input_tokens"] += metrics["input_tokens"]

                session_totals["output_tokens"] += metrics["output_tokens"]

                session_totals["thought_tokens"] += metrics["thought_tokens"]

                session_totals["cached_tokens"] += metrics["cached_tokens"]

                session_totals["total_tokens"] += metrics["total_tokens"]

                session_totals["estimated_cost"] += (
                    metrics["estimated_paid_tier_cost"]
                )

                display_session_usage(session_totals)

        except EOFError:

            print("\nInput stream closed. Exiting application.")

            display_session_usage(session_totals)

            break


# 9. Application entry point
if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        print("\n\nApplication interrupted. Goodbye!")

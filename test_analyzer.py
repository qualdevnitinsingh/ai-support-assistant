from analyzer import analyze_customer_message

message="   "

result = analyze_customer_message(message)

print(result.model_dump_json(indent=2))
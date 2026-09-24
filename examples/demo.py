from open_system_one import DecisionEngine
from open_system_one.backends.mock import FixedBackend
from open_system_one.schema import DecisionRequest

request = DecisionRequest.model_validate({
    "state": "The invoice was charged twice this month.",
    "questions": {
        "is_billing": {"type": "noul", "instructions": "Is this a billing issue?"},
        "team": {
            "type": "choice",
            "instructions": "Which team should handle it?",
            "criteria": {
                "billing": "charges and refunds",
                "shipping": "delivery problems",
                "account": "login/profile",
            },
        },
        "urgency": {
            "type": "score",
            "instructions": "How urgent is it?",
            "criteria": ["routine", "same day", "immediate"],
        },
    },
})
print(DecisionEngine(FixedBackend()).evaluate(request).model_dump_json(indent=2))

from client import ErrandActionDispatcher

dispatcher = ErrandActionDispatcher()

# Dispatch a lunch order
errand = dispatcher.create_errand("ORDER_LUNCH", {"restaurant": "Sweetgreen", "items": ["Harvest Bowl"]})
print("Errand Created:", errand["errand_id"], errand["state"])

# Transit to IN_TRANSIT
dispatcher.transition(errand["errand_id"], "IN_TRANSIT", "Driver picked up package")

# Complete errand
dispatcher.transition(errand["errand_id"], "COMPLETED", "Delivered to reception")

summary = dispatcher.get_summary(errand["errand_id"])
print("Final Summary:", summary)

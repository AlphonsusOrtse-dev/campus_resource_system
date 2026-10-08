import json

def load_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "resources": [],
            "fellows": {},
            "borrow_records": []
        }


def save_data(resources, fellows, borrow_records):
    data = {
        "resources": resources,
        "fellows": fellows,
        "borrow_records": borrow_records
    }

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

resources = [
    {
        "id": "R001",
        "name": "Laptop",
        "category": "Electronics",
        "total": 10,
        "available": 10
    },
    {
        "id": "R002",
        "name": "Keyboard",
        "category": "Accessories",
        "total": 5,
        "available": 5
    },
    {
        "id": "R003",
        "name": "Headset",
        "category": "Accessories",
        "total": 3,
        "available": 3
    }
]

fellows = {
    "F001": "Ada",
    "F002": "John",
    "F003": "Grace"
}

borrow_records = []


def find_resource(resource_id):
    """Find and return a resource by ID."""
    for resource in resources:
        if resource["id"].upper() == resource_id.upper():
            return resource

    return None


def display_resource(resource):
    """Display one resource in a readable format."""
    borrowed = resource["total"] - resource["available"]

    print(
        f'{resource["id"]} | '
        f'{resource["name"]} | '
        f'{resource["category"]} | '
        f'Total: {resource["total"]} | '
        f'Available: {resource["available"]} | '
        f'Borrowed: {borrowed}'
    )


def list_resources():
    """Display all resources."""
    print("\n--- RESOURCE INVENTORY ---")

    if not resources:
        print("No resources available.")
        return

    for resource in resources:
        display_resource(resource)


def add_resource():
    """Add a new resource after validating its details."""
    print("\n--- ADD RESOURCE ---")

    resource_id = input("Resource ID: ").strip().upper()

    if not resource_id:
        print("Error: Resource ID cannot be empty.")
        return

    if find_resource(resource_id) is not None:
        print(f"Error: Resource ID {resource_id} already exists.")
        return

    name = input("Resource name: ").strip()

    if not name:
        print("Error: Resource name cannot be empty.")
        return

    category = input("Category: ").strip()

    if not category:
        print("Error: Category cannot be empty.")
        return

    try:
        total = int(input("Total units: ").strip())
    except ValueError:
        print("Error: Total units must be a whole number.")
        return

    if total <= 0:
        print("Error: Total units must be greater than zero.")
        return

    resource = {
        "id": resource_id,
        "name": name,
        "category": category,
        "total": total,
        "available": total
    }

    resources.append(resource)

    print(f"Resource {name} added successfully.")


def borrow_resource():
    """Borrow a resource if all borrowing rules are satisfied."""
    print("\n--- BORROW RESOURCE ---")

    fellow_id = input("Fellow ID: ").strip().upper()

    if fellow_id not in fellows:
        print(f"Error: Fellow {fellow_id} does not exist.")
        return

    resource_id = input("Resource ID: ").strip().upper()

    resource = find_resource(resource_id)

    if resource is None:
        print(f"Error: Resource {resource_id} does not exist.")
        return

    try:
        quantity = int(input("Quantity: ").strip())
    except ValueError:
        print("Error: Quantity must be a positive integer.")
        return

    if quantity <= 0:
        print("Error: Quantity must be greater than zero.")
        return

    if quantity > resource["available"]:
        print(
            f"Error: Only {resource['available']} "
            f"{resource['name']} unit(s) are available."
        )
        return

    # All validation has passed.
    # Now it is safe to modify the application state.
    resource["available"] -= quantity

    borrow_records.append(
        {
            "fellow_id": fellow_id,
            "resource_id": resource["id"],
            "quantity": quantity
        }
    )

    print(
        f"{fellows[fellow_id]} successfully borrowed "
        f"{quantity} {resource['name']}(s)."
    )
    print(f"Available units remaining: {resource['available']}")


def find_borrow_record(fellow_id, resource_id):
    """Find a fellow's borrowing record for a specific resource."""
    for record in borrow_records:
        if (
            record["fellow_id"] == fellow_id
            and record["resource_id"] == resource_id
        ):
            return record

    return None


def return_resource():
    """Return resources currently held by a fellow."""
    print("\n--- RETURN RESOURCE ---")

    fellow_id = input("Fellow ID: ").strip().upper()

    if fellow_id not in fellows:
        print(f"Error: Fellow {fellow_id} does not exist.")
        return

    resource_id = input("Resource ID: ").strip().upper()

    resource = find_resource(resource_id)

    if resource is None:
        print(f"Error: Resource {resource_id} does not exist.")
        return

    try:
        quantity = int(input("Quantity: ").strip())
    except ValueError:
        print("Error: Quantity must be a positive integer.")
        return

    if quantity <= 0:
        print("Error: Quantity must be greater than zero.")
        return

    record = find_borrow_record(fellow_id, resource["id"])

    if record is None:
        print(
            f"Error: {fellows[fellow_id]} does not currently "
            f"have {resource['name']} on loan."
        )
        return

    if quantity > record["quantity"]:
        print(
            f"Error: {fellows[fellow_id]} only has "
            f"{record['quantity']} {resource['name']}(s) on loan."
        )
        return

    # All validation has passed.
    # Now it is safe to modify the application state.
    resource["available"] += quantity
    record["quantity"] -= quantity

    if record["quantity"] == 0:
        borrow_records.remove(record)

    print(
        f"{fellows[fellow_id]} successfully returned "
        f"{quantity} {resource['name']}(s)."
    )
    print(f"Available units now: {resource['available']}")


def search_resources():
    """Search resources by name without considering letter case."""
    print("\n--- SEARCH RESOURCES ---")

    search_term = input("Enter resource name: ").strip().lower()

    if not search_term:
        print("Error: Search term cannot be empty.")
        return

    matches = []

    for resource in resources:
        if search_term in resource["name"].lower():
            matches.append(resource)

    if not matches:
        print("No resources found.")
        return

    print("\nSearch results:")

    for resource in matches:
        display_resource(resource)


def filter_by_category():
    """Display resources belonging to a selected category."""
    print("\n--- FILTER BY CATEGORY ---")

    category = input("Enter category: ").strip().lower()

    if not category:
        print("Error: Category cannot be empty.")
        return

    matches = []

    for resource in resources:
        if resource["category"].lower() == category:
            matches.append(resource)

    if not matches:
        print("No resources found in that category.")
        return

    print("\nMatching resources:")

    for resource in matches:
        display_resource(resource)


def generate_report():
    """Generate the required inventory report."""
    print("\n--- INVENTORY REPORT ---")

    total_units = sum(
        resource["total"]
        for resource in resources
    )

    available_units = sum(
        resource["available"]
        for resource in resources
    )

    borrowed_units = total_units - available_units

    print(f"Total units: {total_units}")
    print(f"Available units: {available_units}")
    print(f"Currently borrowed: {borrowed_units}")

    print("\nLow-stock resources (fewer than 3 available):")

    low_stock = [
        resource
        for resource in resources
        if resource["available"] < 3
    ]

    if low_stock:
        for resource in low_stock:
            print(
                f"- {resource['name']}: "
                f"{resource['available']} available"
            )
    else:
        print("None")

    borrowed_by_resource = []

    for resource in resources:
        borrowed = resource["total"] - resource["available"]

        borrowed_by_resource.append(
            {
                "resource": resource,
                "borrowed": borrowed
            }
        )

    if borrowed_by_resource:
        maximum_borrowed = max(
            item["borrowed"]
            for item in borrowed_by_resource
        )

        leaders = [
            item
            for item in borrowed_by_resource
            if item["borrowed"] == maximum_borrowed
        ]

        print("\nMost borrowed resource(s):")

        for leader in leaders:
            print(
                f"- {leader['resource']['name']}: "
                f"{leader['borrowed']} borrowed"
            )
    else:
        print("\nMost borrowed resource(s): None")


def display_menu():
    """Display the application's main menu."""
    print("\n" + "=" * 45)
    print(" CAMPUS RESOURCE MANAGEMENT SYSTEM")
    print("=" * 45)
    print("1. Add resource")
    print("2. List resources")
    print("3. Borrow resource")
    print("4. Return resource")
    print("5. Search resources")
    print("6. Filter by category")
    print("7. Generate report")
    print("8. Exit")
    print("=" * 45)


def main():
    """Run the application until the user chooses to exit."""
    while True:
        display_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_resource()

        elif choice == "2":
            list_resources()

        elif choice == "3":
            borrow_resource()

        elif choice == "4":
            return_resource()

        elif choice == "5":
            search_resources()

        elif choice == "6":
            filter_by_category()

        elif choice == "7":
            generate_report()

        elif choice == "8":
            print("Thank you for using the Campus Resource Management System.")
            break

        else:
            print("Error: Please choose a number from 1 to 8.")


if __name__ == "__main__":
    main()
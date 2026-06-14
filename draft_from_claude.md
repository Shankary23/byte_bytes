# UML Class Diagram — ByteBites Backend

## Class Diagram

```
┌─────────────────────────────┐         ┌─────────────────────────────┐
│           Customer          │         │           FoodItem           │
├─────────────────────────────┤         ├─────────────────────────────┤
│ - name: String              │         │ - name: String              │
│ - purchase_history: List    │         │ - price: Float              │
├─────────────────────────────┤         │ - category: String          │
│ + verify_user(): Boolean    │         │ - popularity_rating: Float  │
└──────────────┬──────────────┘         └──────┬──────────────────────┘
               │ 1                             │ *             │ *
               │ places                        │ contained in  │ listed in
               │ *                             │               │
┌──────────────▼──────────────┐         ┌──────▼──────────────────────┐
│            Order            │◄────────│            Menu             │
├─────────────────────────────┤  * uses ├─────────────────────────────┤
│ - items: List[FoodItem]     │    1    │ - items: List[FoodItem]     │
│ - customer: Customer        │         ├─────────────────────────────┤
├─────────────────────────────┤         │ + add_item(item): void      │
│ + compute_total(): Float    │         │ + filter_by_category(       │
└──────────────┬──────────────┘         │     category: String        │
               │ *                      │   ): List[FoodItem]         │
               │ contains               └─────────────────────────────┘
               │ *
               ▼
         [FoodItem] (see above)
```

**Relationship summary:**
- `Customer` (1) ──places──► `Order` (*)
- `Order` (*) ──contains──► `FoodItem` (*)
- `Menu` (1) ──holds──► `FoodItem` (*)
- `Menu` (1) ──sources items into──► `Order` (*)

---

## Class Descriptions

### Customer
| Member | Type | Notes |
|---|---|---|
| `name` | String | Customer's display name |
| `purchase_history` | List[Order] | All past orders |
| `verify_user()` | → Boolean | Confirms user is real/registered |

### FoodItem
| Member | Type | Notes |
|---|---|---|
| `name` | String | e.g. "Spicy Burger" |
| `price` | Float | Unit price |
| `category` | String | e.g. "Drinks", "Desserts" |
| `popularity_rating` | Float | Ranking metric |

### Menu
| Member | Type | Notes |
|---|---|---|
| `items` | List[FoodItem] | Full catalog of available food items |
| `add_item(item)` | → void | Adds a FoodItem to the catalog |
| `filter_by_category(category)` | → List[FoodItem] | Returns items matching the given category |

### Order (Transaction)
| Member | Type | Notes |
|---|---|---|
| `items` | List[FoodItem] | Items selected by the customer |
| `customer` | Customer | The placing customer |
| `compute_total()` | → Float | Sums `price` across all items |

---

## Relationships

| From | Relationship | To | Multiplicity | Notes |
|---|---|---|---|---|
| Customer | places | Order | 1 → many | A customer can have many orders |
| Order | contains | FoodItem | many ↔ many | Many orders can share the same item; one order holds many items |
| Menu | holds | FoodItem | 1 → many | The menu is the master catalog of all food items |
| Menu | sources items into | Order | 1 → many | Customers pick items from the menu to add to an order |

---

## Design Notes

### Why these four classes were chosen

| Class | Justification |
|---|---|
| `Customer` | The spec explicitly requires tracking users by name and purchase history, and confirming they are real — a concrete, persistent entity with identity and state. |
| `FoodItem` | The spec lists specific data to track per item (name, price, category, popularity rating) — a clear, well-bounded data object. |
| `Menu` | The spec asks for "a digital list that holds all items and lets us filter by category" — a container/manager object with its own behavior (filtering), not just a raw list. |
| `Order` | The spec calls for a "transaction object" that groups selected items and computes total cost — a distinct entity that models a real-world event. |

### Why the candidate names were excluded

The spec's "Candidate Classes" listed: **Relient, Scalable, Functional, Fast**.

These are excluded because they describe *qualities* or *design goals* of the system, not *entities* with data and behavior. In UML class modeling, a class must represent a noun — a thing that has attributes and can do something. Adjectives like "scalable" or "fast" describe how the system should perform, not what objects exist within it. None of these candidates have attributes, methods, or relationships that map to the domain — they belong in a requirements or non-functional specification document, not a class diagram.

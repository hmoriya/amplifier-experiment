# Chapter 21: Aggregate Design — The Castle Walls of Consistency

## The Medieval Castle: A Perfect Metaphor

Imagine standing before a medieval castle. Its massive stone walls rise from the earth, creating a clear boundary between the protected inner world and the chaos outside. The single drawbridge serves as the only point of entry, carefully controlled by guards who ensure that only legitimate visitors may enter. Inside these walls, order prevails—the lord's word is law, rules are enforced consistently, and every inhabitant knows their place in the hierarchy.

This is exactly how aggregates work in domain-driven design. They are the castle walls of your domain model, protecting the consistency of your business rules and maintaining order within their boundaries.

## What Aggregates Protect and Why

### The Sacred Grounds of Business Invariants

Just as a castle protects its treasures, an aggregate protects business invariants—those rules that must never be violated. Consider a shopping cart:

- **The Treasury Rule**: A cart cannot contain more than 50 different types of items (prevents system abuse)
- **The Guard Rule**: Only active carts can be modified (protects data integrity)
- **The Accounting Rule**: Item quantities must be positive numbers (maintains logical consistency)

These aren't just technical constraints—they're the fundamental laws that keep your business domain coherent. Break them, and chaos ensues, much like allowing enemies through the castle gates.

### The Single Point of Truth

In our castle metaphor, the lord of the castle serves as the aggregate root—the single authority through which all changes must pass. Just as peasants cannot directly modify castle laws but must petition the lord, external code cannot directly modify entities within an aggregate but must go through the aggregate root.

This creates a powerful guarantee: if you want to know the state of anything within the aggregate, you need only ask the aggregate root. It maintains the single source of truth for its entire domain.

## Finding the Right Boundaries

### The Art of Wall Placement

Where should you place your castle walls? Too small, and you'll have a village of tiny fortresses that can't protect anything meaningful. Too large, and you'll have an unwieldy empire that's impossible to defend effectively.

Consider an e-commerce system. You might be tempted to create one massive "Order" aggregate that includes:
- The customer details
- All order items
- Payment information
- Shipping details
- Invoice history
- Return records

This would be like trying to build walls around an entire kingdom—impractical and inefficient. Instead, we look for natural boundaries.

### The Natural Boundaries Exercise

To find aggregate boundaries, ask yourself:

1. **What must change together?** Items in a shopping cart must be modified as a unit when checking out.
2. **What has a shared lifecycle?** Cart items are created and destroyed with their cart.
3. **What rules span multiple entities?** The "maximum 50 items" rule affects the entire cart.
4. **What needs transactional consistency?** All cart modifications must succeed or fail together.

These questions reveal that a Shopping Cart and its Items form a natural aggregate, while Customer, Payment, and Shipping are separate aggregates with their own castle walls.

## The Balance Between Fortresses

### Why Small Aggregates Win

Small aggregates are like nimble fortresses—easy to defend, quick to mobilize, and rarely in each other's way. They offer:

1. **Better Concurrency**: Multiple users can modify different aggregates simultaneously without conflict
2. **Improved Performance**: Loading a small aggregate is faster than loading a sprawling empire
3. **Clearer Boundaries**: It's obvious what belongs inside and what stays outside
4. **Simpler Testing**: You can verify the aggregate's behavior in isolation

### The Cost of Coordination

But small aggregates come with a price: coordination. When you need multiple aggregates to work together, you can't simply reach across castle walls. Instead, you must use:

- **Messages** (Events): "The cart has been checked out!"
- **Ambassadors** (Domain Services): Orchestrating between aggregates
- **Treaties** (Eventual Consistency): Accepting that perfect synchronization isn't always necessary

## Real-World Design Decisions

### The Shopping Cart Saga

Let's explore how these principles apply to a real shopping cart:

**What's Inside the Castle Walls:**
- The cart's identity and status
- All items with their quantities and prices
- The customer ID (not the customer!)
- Business rules about cart validity

**What's Outside:**
- Product details (referenced by ID)
- Customer information (in the Customer aggregate)
- Inventory levels (in the Inventory aggregate)
- Payment processing (in the Payment aggregate)

This design allows multiple customers to shop simultaneously without interfering with each other, while still maintaining strict consistency within each cart.

### The Order Fulfillment Dance

When a customer checks out, watch how aggregates coordinate like allied castles:

1. **Shopping Cart Castle**: "I'm checking out! Here's what I contain."
2. **Inventory Castle**: "I'll reserve these items for you."
3. **Payment Castle**: "I'll process the payment."
4. **Shipping Castle**: "I'll prepare for dispatch."

Each castle maintains its own consistency while cooperating through well-defined protocols. If payment fails, the inventory castle can release its reservations—no castle is left in an inconsistent state.

## The Tension Between Ideal and Reality

### The Purist's Dream vs. The Pragmatist's Reality

In an ideal world, every aggregate would be perfectly small, every boundary crystal clear, and every interaction elegantly coordinated through events. Reality is messier:

- **Legacy Constraints**: That old order table with 47 columns isn't going anywhere
- **Performance Pressures**: Sometimes you need that data NOW, not eventually
- **Team Understanding**: Not everyone grips eventual consistency immediately
- **Business Expectations**: "But it worked instantly in the old system!"

### Making Pragmatic Choices

The key is to make conscious trade-offs:

1. **Start Ideal**: Design small, focused aggregates first
2. **Measure Reality**: Profile performance and identify bottlenecks
3. **Optimize Carefully**: Denormalize read models before breaking aggregate boundaries
4. **Document Decisions**: Future developers need to understand why you bent the rules

## Visual Patterns for Aggregate Design

### The Boundary Map

Draw your aggregates as actual castles:
```
┌─────────────────────┐     ┌─────────────────────┐
│   Shopping Cart     │     │     Inventory       │
│  ┌─────────────┐    │     │  ┌─────────────┐    │
│  │ Cart Items  │    │────▶│  │  Products   │    │
│  └─────────────┘    │ ID  │  └─────────────┘    │
└─────────────────────┘     └─────────────────────┘
         │                            │
         │ Events                     │ Events
         ▼                            ▼
    ┌─────────────────────────────────────┐
    │          Event Bus                   │
    └─────────────────────────────────────┘
```

### The Lifecycle Timeline

Visualize aggregate interactions over time:
```
Cart          Inventory       Payment        Shipping
 │                │              │              │
 ├─Create────────┤              │              │
 │                │              │              │
 ├─Add Items─────┤              │              │
 │                │              │              │
 ├─Checkout──────┼──Reserve────▶│              │
 │                │              │              │
 │                │         ┌────┼─Process     │
 │                │         │    │              │
 │                │◀────────┘    │         ┌───┤
 │                │              │         │   │
 │                ├─Confirm─────▶│         │   │
 │                │              │         │   │
 │                │              │◀────────┘   │
 │                │              │             │
```

## Summary: The Wisdom of Walls

Aggregate design is about drawing the right boundaries—not too big, not too small, but just right for your domain's needs. Like medieval castle builders, we must:

1. **Protect What Matters**: Identify and guard your business invariants
2. **Control Access**: Channel all changes through aggregate roots
3. **Right-Size Your Fortresses**: Keep aggregates as small as possible but as large as necessary
4. **Coordinate Kingdoms**: Use events and services for inter-aggregate collaboration
5. **Balance Idealism with Pragmatism**: Make conscious trade-offs when needed

Remember: The walls you draw today will shape how your system grows tomorrow. Choose wisely, document thoroughly, and always keep the drawbridge well-guarded.

## Practice Exercises

### Exercise 1: Hotel Reservation System

Design aggregates for a hotel with:
- Rooms that can be reserved
- Reservations with check-in/check-out dates
- Guests with contact information
- Policies about overbooking and cancellations

**Questions to Consider:**
- Should Room and Reservation be one aggregate or two?
- How do you prevent double-booking?
- Where do cancellation policies live?

### Exercise 2: Inventory Management

Design aggregates for a warehouse system handling:
- Products with stock levels
- Incoming shipments
- Outgoing orders
- Stock transfers between locations
- Inventory audits

**Challenges:**
- How do you handle concurrent stock updates?
- What's the aggregate boundary for a stock transfer?
- How do you maintain consistency during audits?

### Exercise 3: Project Management Decomposition

You have a large "Project" aggregate containing:
- Project details
- All tasks and subtasks
- Team members and roles
- Progress tracking
- Documents and attachments
- Comments and discussions

**Your Mission:**
Break this down into appropriately-sized aggregates while maintaining business invariants like:
- Tasks must belong to a project
- Progress must reflect task completion
- Team members must have defined roles

## Next Chapter Preview

Now that we understand how to build strong castle walls around our aggregates, Chapter 22 will explore CQRS and Event Sourcing—advanced patterns that let us optimize how we read from and write to these fortified domains. We'll learn how to separate the concerns of commanding our castle (writes) from surveying our kingdom (reads).

---

*Remember: Every great castle started with a simple question—what needs protecting? Answer that, and the walls will reveal themselves.*
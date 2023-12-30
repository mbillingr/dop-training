
A Simple Game
=============

I'm learning Data Oriented Programming by following the book using my own 
example project: a little game similar to those multi-player browser games
popular in the early 2000s.

Essential Mechanics
-------------------

- 3 Units (Rock/Paper/Scissors)
  1. Stationary Defense (>> 3.)
  2. Siege Unit (>> 1.)
  3. Siege Breaker (>> 2.)
- Colonize locations
- Build Base (increasing cost/duration)
  - Civilian Infrastructure -> Population
  - Mining Infrastructure -> Materials
  - Production Infrastructure -> Base/Units
- Build Units
- Send Fleets
  - At most one faction at location
  - Max nr of fleets in transit
  - Launch costs resources?


DOP
===

Data Entities
-------------

- Game
  - Star System
    - Buildings
    - Ships
  - Player
    - Home System
    - Fleets
  - Event
    - ETA
    - Event type
    - Event data

Data Model
----------
- Game
  - star_systems_by_id: {StarSystem}
  - players_by_id: {Player}
  - events: [Event]
- Player
  - home_system_id: SystemId
  - fleets: [Fleet]
- StarSystem
  - owning_player: PlayerId  # infrastructure owner
  - controlling_player: PlayerId  # military presence owner
  - buildings: {int}
  - ships: {int}
  - building_slot: [Event]
- Event
  - eta: DateTime
  - type: tba?
  - data: tba?

Code
----

### Game
- get system owning player
- list buildings
- list ships
- build infrastructure
- build ship
- send fleet
- colonize
- get home system
- list fleets
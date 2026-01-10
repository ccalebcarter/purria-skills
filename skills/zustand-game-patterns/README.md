# Zustand Game Patterns

Zustand state management patterns optimized for games.

## Expertise

This skill provides:

- **Store Architecture**: Organizing game state
- **Persistence**: Save/load systems
- **Undo/Redo**: Action history
- **Time-Travel Debugging**: State inspection
- **Subscriptions**: Efficient UI updates
- **Performance**: Minimizing re-renders
- **Immer Integration**: Immutable updates made easy

## When to Use

Invoke this skill when you need to:

- Design game state architecture
- Implement save/load functionality
- Add undo/redo to actions
- Debug state issues
- Optimize re-renders
- Sync state with server

## Store Patterns

### Basic Game Store

```typescript
import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

interface GameState {
  player: {
    coins: number;
    level: number;
    inventory: Item[];
  };
  actions: {
    addCoins: (amount: number) => void;
    addItem: (item: Item) => void;
    levelUp: () => void;
  };
}

export const useGameStore = create<GameState>()(
  immer((set) => ({
    player: {
      coins: 0,
      level: 1,
      inventory: [],
    },
    actions: {
      addCoins: (amount) =>
        set((state) => {
          state.player.coins += amount;
        }),
      addItem: (item) =>
        set((state) => {
          state.player.inventory.push(item);
        }),
      levelUp: () =>
        set((state) => {
          state.player.level += 1;
        }),
    },
  }))
);
```

### Persisted Store (Save/Load)

```typescript
import { persist } from "zustand/middleware";

export const useGameStore = create<GameState>()(
  persist(
    immer((set) => ({
      // ... state and actions
    })),
    {
      name: "game-save",
      partialize: (state) => ({
        player: state.player,
        // Don't persist UI state
      }),
    }
  )
);
```

### Sliced Store (Large Games)

```typescript
// playerSlice.ts
export const createPlayerSlice = (set, get) => ({
  player: { coins: 0 },
  addCoins: (n) => set((s) => { s.player.coins += n }),
});

// inventorySlice.ts
export const createInventorySlice = (set, get) => ({
  inventory: [],
  addItem: (item) => set((s) => { s.inventory.push(item) }),
});

// store.ts
export const useGameStore = create()(
  immer((...a) => ({
    ...createPlayerSlice(...a),
    ...createInventorySlice(...a),
  }))
);
```

## Subscription Patterns

### Selective Subscriptions

```typescript
// Only re-render when coins change
const coins = useGameStore((state) => state.player.coins);

// Multiple values with shallow compare
const { coins, level } = useGameStore(
  (state) => ({ coins: state.player.coins, level: state.player.level }),
  shallow
);
```

### Outside React

```typescript
// Subscribe to changes outside components
const unsubscribe = useGameStore.subscribe(
  (state) => state.player.coins,
  (coins) => {
    console.log("Coins changed:", coins);
    // Update UI, play sound, etc.
  }
);
```

## Undo/Redo Pattern

```typescript
interface UndoState<T> {
  past: T[];
  present: T;
  future: T[];
  set: (state: T) => void;
  undo: () => void;
  redo: () => void;
}

const useUndoStore = create<UndoState<GameData>>()(
  immer((set) => ({
    past: [],
    present: initialState,
    future: [],
    set: (newState) =>
      set((state) => {
        state.past.push(state.present);
        state.present = newState;
        state.future = [];
      }),
    undo: () =>
      set((state) => {
        if (state.past.length === 0) return;
        state.future.unshift(state.present);
        state.present = state.past.pop()!;
      }),
    redo: () =>
      set((state) => {
        if (state.future.length === 0) return;
        state.past.push(state.present);
        state.present = state.future.shift()!;
      }),
  }))
);
```

## Performance Tips

### Avoid Over-Subscriptions

```typescript
// Bad: Re-renders on ANY state change
const state = useGameStore();

// Good: Only re-renders when coins change
const coins = useGameStore((s) => s.player.coins);
```

### Use Actions Object

```typescript
// Actions don't cause re-renders when destructured
const { addCoins, addItem } = useGameStore((s) => s.actions);
```

### Memoize Derived State

```typescript
const selectTotalValue = (state) =>
  state.inventory.reduce((sum, item) => sum + item.value, 0);

// In component
const totalValue = useGameStore(selectTotalValue);
```

## Integration

This skill works alongside:

- `drizzle-game-schema` - Server state sync
- `react-game-ui` - Consuming state
- `testing-team` - Testing stores

## Usage in Claude Code

```
/zustand-game-patterns

"Design state architecture for farming game..."
"Implement save/load with persistence..."
"Add undo/redo to crop planting..."
```

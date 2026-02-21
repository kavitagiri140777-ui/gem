# Frontend component: ParkBidFinder

This folder contains a React component (`ParkBidFinder.tsx`) for a mobile-first dashboard UI aimed at Park Enterprises.

## What it shows
- Bid list cards with score, buyer, value, and deadline.
- Details page on click with matched keywords and action buttons.
- Keywords include requested items like `safety nets`, `safety posters`, and `acrylic boards`.

## How to use
Import `ParkBidFinder` into your React app and render it in a page/component:

```tsx
import ParkBidFinder from "./frontend/ParkBidFinder";

export default function App() {
  return <ParkBidFinder />;
}
```

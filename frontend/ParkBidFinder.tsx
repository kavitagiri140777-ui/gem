import { useState } from "react";

type BidItem = {
  id: number;
  bidNumber: string;
  title: string;
  buyer: string;
  value: string;
  deadline: string;
  score: number;
  keywords: string[];
};

const bidsData: BidItem[] = [
  {
    id: 1,
    bidNumber: "GEM/2026/B/510002",
    title: "Supply & Installation of Safety Nets",
    buyer: "Naval Dockyard Visakhapatnam",
    value: "₹12.4 Lakh",
    deadline: "12 Mar 2026",
    score: 94,
    keywords: ["safety nets", "installation", "dock"],
  },
  {
    id: 2,
    bidNumber: "GEM/2026/B/510001",
    title: "Acrylic Safety Sign Boards",
    buyer: "Indian Navy",
    value: "₹8.2 Lakh",
    deadline: "18 Mar 2026",
    score: 88,
    keywords: ["acrylic boards", "safety posters", "safety"],
  },
];

function Card(props: React.HTMLAttributes<HTMLDivElement>) {
  return <div {...props} style={{ border: "1px solid #e5e7eb", borderRadius: 16, background: "white", ...(props.style || {}) }} />;
}

function CardContent(props: React.HTMLAttributes<HTMLDivElement>) {
  return <div {...props} />;
}

function Button(props: React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "outline" | "secondary" }) {
  const variantStyle =
    props.variant === "outline"
      ? { background: "white", border: "1px solid #d1d5db" }
      : props.variant === "secondary"
      ? { background: "#e5e7eb", border: "1px solid #d1d5db" }
      : { background: "#111827", color: "white", border: "1px solid #111827" };
  return <button {...props} style={{ padding: "8px 12px", borderRadius: 10, cursor: "pointer", ...variantStyle, ...(props.style || {}) }} />;
}

export default function ParkBidFinder() {
  const [selectedBid, setSelectedBid] = useState<BidItem | null>(null);

  if (selectedBid) {
    return (
      <div style={{ padding: 16, display: "grid", gap: 16 }}>
        <Button variant="outline" onClick={() => setSelectedBid(null)}>
          ← Back
        </Button>
        <Card style={{ boxShadow: "0 8px 24px rgba(0,0,0,.08)" }}>
          <CardContent style={{ padding: 16 }}>
            <h2 style={{ fontSize: 24, margin: "0 0 8px" }}>{selectedBid.title}</h2>
            <p><b>Bid No:</b> {selectedBid.bidNumber}</p>
            <p><b>Buyer:</b> {selectedBid.buyer}</p>
            <p><b>Value:</b> {selectedBid.value}</p>
            <p><b>Deadline:</b> {selectedBid.deadline}</p>
            <p><b>Score:</b> {selectedBid.score}%</p>
            <div>
              <b>Matched keywords:</b>
              <ul style={{ marginLeft: 20 }}>
                {selectedBid.keywords.map((k) => (
                  <li key={k}>{k}</li>
                ))}
              </ul>
            </div>
            <div style={{ display: "flex", gap: 8, paddingTop: 8 }}>
              <Button>Download BOQ</Button>
              <Button variant="secondary">Open in GeM</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div style={{ padding: 16, display: "grid", gap: 16 }}>
      <h1 style={{ fontSize: 32, margin: 0 }}>Park Bid Finder</h1>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 8 }}>
        <Card><CardContent style={{ padding: 12, textAlign: "center" }}>⭐ High 5</CardContent></Card>
        <Card><CardContent style={{ padding: 12, textAlign: "center" }}>✅ Good 8</CardContent></Card>
        <Card><CardContent style={{ padding: 12, textAlign: "center" }}>📅 Closing 3</CardContent></Card>
      </div>

      <div style={{ display: "grid", gap: 12 }}>
        {bidsData.map((bid) => (
          <Card
            key={bid.id}
            style={{ cursor: "pointer", boxShadow: "0 2px 8px rgba(0,0,0,.06)" }}
            onClick={() => setSelectedBid(bid)}
          >
            <CardContent style={{ padding: 16 }}>
              <h2 style={{ margin: "0 0 8px", fontSize: 18 }}>{bid.title}</h2>
              <p style={{ margin: "0 0 4px", color: "#4b5563" }}>Bid No: {bid.bidNumber}</p>
              <p style={{ margin: "0 0 4px", color: "#4b5563" }}>{bid.buyer}</p>
              <p style={{ margin: "0 0 4px" }}>{bid.value}</p>
              <p style={{ margin: "0 0 4px" }}>Deadline: {bid.deadline}</p>
              <p style={{ margin: 0, fontWeight: 700 }}>Score {bid.score}%</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

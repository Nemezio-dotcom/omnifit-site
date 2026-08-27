import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import Competitors from "./pages/Competitors";
import Dashboard from "./pages/Dashboard";
import OpportunityDetail from "./pages/OpportunityDetail";
import Opportunities from "./pages/Opportunities";
import PageDetail from "./pages/PageDetail";
import PagesList from "./pages/PagesList";
import Simulator from "./pages/Simulator";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/pages" element={<PagesList />} />
        <Route path="/pages/:pageId" element={<PageDetail />} />
        <Route path="/opportunities" element={<Opportunities />} />
        <Route path="/opportunities/:opportunityId" element={<OpportunityDetail />} />
        <Route path="/simulator" element={<Simulator />} />
        <Route path="/competitors" element={<Competitors />} />
      </Route>
    </Routes>
  );
}

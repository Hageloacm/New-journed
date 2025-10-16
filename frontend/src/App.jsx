import React, { useState } from "react";
import Dashboard from "./components/Dashboard";
import UsersTable from "./components/UsersTable";
import Transactions from "./components/Transactions";

export default function App() {
  const [tab, setTab] = useState("dashboard");
  return (
    <div style={{padding:20, fontFamily:"Arial"}}>
      <h1>OLAF ADMIN</h1>
      <div style={{marginBottom:10}}>
        <button onClick={()=>setTab("dashboard")}>Dashboard</button>
        <button onClick={()=>setTab("users")}>Usuários</button>
        <button onClick={()=>setTab("tx")}>Transações</button>
      </div>
      {tab === "dashboard" && <Dashboard />}
      {tab === "users" && <UsersTable />}
      {tab === "tx" && <Transactions />}
    </div>
  );
}
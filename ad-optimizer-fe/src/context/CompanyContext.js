// src/context/CompanyContext.js
import React, { createContext, useState, useContext } from "react";

const CompanyContext = createContext();

export const useCompany = () => {
  return useContext(CompanyContext);
};

export const CompanyProvider = ({ children }) => {
  const [companyId, setCompanyId] = useState("");
  const [propertyId, setPropertyId] = useState(""); // New propertyId state

  return (
    <CompanyContext.Provider
      value={{ companyId, setCompanyId, propertyId, setPropertyId }}
    >
      {children}
    </CompanyContext.Provider>
  );
};

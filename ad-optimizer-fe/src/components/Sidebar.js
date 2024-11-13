// src/components/Sidebar.js
import React, { useState, useEffect } from "react";
import {
  Drawer,
  List,
  ListItem,
  Select,
  MenuItem,
  Button,
  Tooltip,
  useMediaQuery,
  CircularProgress,
  Typography,
} from "@mui/material";
import { AddCircle, Business } from "@mui/icons-material";
import { useCompany } from "../context/CompanyContext";
import axios from "axios";
import CreateCompanyModal from "./CreateCompanyModal";
import CreatePropertyModal from "./CreatePropertyModal";

const Sidebar = ({ onCreateProperty }) => {
  const { companyId, setCompanyId, propertyId, setPropertyId } = useCompany();
  const [companies, setCompanies] = useState([]);
  const [properties, setProperties] = useState([]);
  const [loadingCompanies, setLoadingCompanies] = useState(true);
  const [loadingProperties, setLoadingProperties] = useState(false);
  const [isCompanyModalOpen, setCompanyModalOpen] = useState(false); // State for modal open/close
  const [isPropertyModalOpen, setPropertyModalOpen] = useState(false); // State for modal open/close
  const isSmallScreen = useMediaQuery((theme) => theme.breakpoints.down("md")); // Adjust breakpoint if needed

  // Fetch companies when the component mounts
  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      console.log("Fetching companies");
      const response = await axios.get("/get-all-companies");
      console.log("🚀 ~ fetchCompanies ~ response:", response);
      setCompanies(response.data);
    } catch (error) {
      console.error("Failed to fetch companies:", error);
    } finally {
      setLoadingCompanies(false);
    }
  };

  // Function to fetch properties - now moved outside useEffect
  const fetchProperties = async (companyId) => {
    console.log("Fetching properties for company:", companyId);
    if (companyId) {
      setLoadingProperties(true);
      try {
        const response = await axios.get(`/get-properties/${companyId}`);
        setProperties(response.data);
        console.log("🚀 ~ fetchProperties ~ response:", response);
      } catch (error) {
        console.error("Failed to fetch properties:", error);
      } finally {
        setLoadingProperties(false);
      }
    } else {
      setProperties([]);
    }
  };

  // UseEffect to fetch properties when the company changes
  useEffect(() => {
    fetchProperties(companyId);
  }, [companyId]);

  // Handle company selection change
  const handleCompanyChange = (e) => {
    const selectedCompanyId = e.target.value;
    setCompanyId(selectedCompanyId);
    setPropertyId(""); // Clear the property selection when the company changes
    fetchProperties(selectedCompanyId); // Fetch properties for the newly selected company
  };

  // Handle property selection change
  const handlePropertyChange = (e) => {
    setPropertyId(e.target.value);
  };

  // Handle saving the new company
  const handleSaveCompany = async (companyData) => {
    try {
      await axios.post("/company", companyData);
      fetchCompanies(); // Refresh the company list after creating a new one
    } catch (error) {
      console.error("Failed to save company:", error);
    }
  };

  // Handle creating a new property
  const handleSaveProperty = async (propertyData) => {
    try {
      await axios.post(
        `/company/${propertyData.company_id}/property`,
        propertyData
      );
    } catch (error) {
      console.error("Failed to create property:", error);
    }
  };

  return (
    <>
      <Drawer
        variant={isSmallScreen ? "temporary" : "permanent"}
        open={!isSmallScreen}
        onClose={() => {}}
        sx={{
          width: "20%",
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: "20%",
            position: "fixed",
            top: 64, // Adjust sidebar's top margin to be below the header
            left: 0,
            bottom: 0,
          },
        }}
      >
        <List>
          {/* Create New Company Button */}
          <ListItem>
            <Tooltip title="Create New Company">
              <Button
                fullWidth
                variant="contained"
                startIcon={<Business />}
                onClick={() => setCompanyModalOpen(true)}
                sx={{ marginBottom: 1 }}
              >
                Create New Company
              </Button>
            </Tooltip>
          </ListItem>

          {/* Create New Property Button */}
          <ListItem>
            <Tooltip title="Create New Property">
              <Button
                fullWidth
                variant="contained"
                startIcon={<AddCircle />}
                onClick={() => setPropertyModalOpen(true)}
                sx={{ marginBottom: 1 }}
              >
                Create New Property
              </Button>
            </Tooltip>
          </ListItem>

          {/* Informative Message */}
          <ListItem>
            <Typography variant="body2" sx={{ padding: 1 }}>
              Please select a company and, optionally, a property for which you
              want to optimize the ad.
            </Typography>
          </ListItem>

          {/* Company Select Field */}
          <ListItem>
            {loadingCompanies ? (
              <CircularProgress />
            ) : (
              <Select
                value={companyId}
                onChange={handleCompanyChange}
                fullWidth
                placeholder="Select Company*"
              >
                <MenuItem value="">Select Company</MenuItem>
                {companies.map((company) => (
                  <MenuItem key={company.company_id} value={company.company_id}>
                    {company.company_name}
                  </MenuItem>
                ))}
              </Select>
            )}
          </ListItem>

          {/* Property Select Field */}
          <ListItem>
            {loadingProperties ? (
              <CircularProgress />
            ) : (
              <Select
                value={propertyId}
                onChange={handlePropertyChange}
                fullWidth
                placeholder="Select Property"
                disabled={!companyId} // Disable property selection until a company is selected
              >
                <MenuItem value="">Select Property</MenuItem>
                {properties.map((property) => (
                  <MenuItem
                    key={property.property_id}
                    value={property.property_id}
                  >
                    {property.property_name}
                  </MenuItem>
                ))}
              </Select>
            )}
          </ListItem>
        </List>
      </Drawer>

      {/* Modal for Creating Company */}
      <CreateCompanyModal
        open={isCompanyModalOpen}
        onClose={() => setCompanyModalOpen(false)}
        onSave={handleSaveCompany}
      />

      {/* Modal for creating  property */}
      <CreatePropertyModal
        open={isPropertyModalOpen}
        onClose={() => setPropertyModalOpen(false)}
        onSave={handleSaveProperty}
      />
    </>
  );
};

export default Sidebar;

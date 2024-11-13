// src/components/CreatePropertyModal.js
import React, { useState, useEffect } from "react";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  Select,
  MenuItem,
  Button,
  CircularProgress,
} from "@mui/material";
import axios from "axios";

const CreatePropertyModal = ({ open, onClose, onSave }) => {
  const [propertyName, setPropertyName] = useState("");
  const [company, setCompany] = useState("");
  const [propertyDetails, setPropertyDetails] = useState("");
  const [companies, setCompanies] = useState([]);
  const [loadingCompanies, setLoadingCompanies] = useState(true);
  const [error, setError] = useState("");

  // Fetch companies when the modal is opened
  useEffect(() => {
    if (open) {
      fetchCompanies();
    }
  }, [open]);

  const fetchCompanies = async () => {
    setLoadingCompanies(true);
    try {
      const response = await axios.get("/get-all-companies");
      setCompanies(response.data);
    } catch (err) {
      console.error("Failed to fetch companies:", err);
    } finally {
      setLoadingCompanies(false);
    }
  };

  const handleSubmit = () => {
    // Validate mandatory fields
    if (!propertyName || !company) {
      setError("Please fill in all required fields.");
      return;
    }

    setError("");
    // Prepare the data to save
    const propertyData = {
      property_name: propertyName,
      company_id: company,
      property_details: propertyDetails,
    };

    // Pass the data back to the parent for further processing (e.g., API call)
    onSave(propertyData);
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Create New Property</DialogTitle>
      <DialogContent>
        <TextField
          label="Property Name"
          fullWidth
          value={propertyName}
          onChange={(e) => setPropertyName(e.target.value)}
          margin="normal"
          required
        />
        {loadingCompanies ? (
          <CircularProgress />
        ) : (
          <Select
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            fullWidth
            margin="normal"
            required
            displayEmpty
          >
            <MenuItem value="">
              <em>Select Company</em>
            </MenuItem>
            {companies.map((company) => (
              <MenuItem key={company.company_id} value={company.company_id}>
                {company.company_name}
              </MenuItem>
            ))}
          </Select>
        )}
        <TextField
          label="Property Details"
          multiline
          rows={4}
          fullWidth
          value={propertyDetails}
          onChange={(e) => setPropertyDetails(e.target.value)}
          margin="normal"
        />
        {error && (
          <div style={{ color: "red", marginTop: "10px" }}>{error}</div>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="secondary">
          Cancel
        </Button>
        <Button onClick={handleSubmit} color="primary" variant="contained">
          Create
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CreatePropertyModal;

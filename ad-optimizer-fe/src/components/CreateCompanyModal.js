// src/components/CreateCompanyModal.js
import React, { useState } from "react";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  Button,
  Box,
  Chip,
  IconButton,
} from "@mui/material";
import { AddCircleOutline } from "@mui/icons-material";

const CreateCompanyModal = ({ open, onClose, onSave }) => {
  const [formData, setFormData] = useState({
    company_id: "",
    company_name: "",
    description: "",
    location: "",
    notable_projects: [],
    popular_locations: [],
    target_market: "",
  });

  const [notableProject, setNotableProject] = useState("");
  const [popularLocation, setPopularLocation] = useState("");

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  // Handle adding a notable project
  const handleAddNotableProject = () => {
    if (notableProject.trim()) {
      setFormData((prevData) => ({
        ...prevData,
        notable_projects: [...prevData.notable_projects, notableProject],
      }));
      setNotableProject("");
    }
  };

  // Handle adding a popular location
  const handleAddPopularLocation = () => {
    if (popularLocation.trim()) {
      setFormData((prevData) => ({
        ...prevData,
        popular_locations: [...prevData.popular_locations, popularLocation],
      }));
      setPopularLocation("");
    }
  };

  // Handle removing a chip (either notable project or popular location)
  const handleDeleteChip = (type, index) => {
    setFormData((prevData) => ({
      ...prevData,
      [type]: prevData[type].filter((_, i) => i !== index),
    }));
  };

  // Handle form submission
  const handleSave = () => {
    // Perform validations if needed
    if (!formData.company_name || !formData.company_id) {
      alert("Company ID and Company Name are required.");
      return;
    }

    onSave(formData);
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md">
      <DialogTitle>Create New Company</DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 2 }}>
          <TextField
            label="Company ID"
            name="company_id"
            value={formData.company_id}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
          />
          <TextField
            label="Company Name"
            name="company_name"
            value={formData.company_name}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
          />
          <TextField
            label="Description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            fullWidth
            margin="normal"
            multiline
            rows={3}
          />
          <TextField
            label="Location"
            name="location"
            value={formData.location}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />

          {/* Notable Projects Section */}
          <Box sx={{ mt: 2 }}>
            <TextField
              label="Add Notable Project"
              value={notableProject}
              onChange={(e) => setNotableProject(e.target.value)}
              fullWidth
              margin="normal"
            />
            <IconButton onClick={handleAddNotableProject} color="primary">
              <AddCircleOutline />
            </IconButton>
            <Box sx={{ display: "flex", flexWrap: "wrap", mt: 1 }}>
              {formData.notable_projects.map((project, index) => (
                <Chip
                  key={index}
                  label={project}
                  onDelete={() => handleDeleteChip("notable_projects", index)}
                  sx={{ margin: "5px" }}
                />
              ))}
            </Box>
          </Box>

          {/* Popular Locations Section */}
          <Box sx={{ mt: 2 }}>
            <TextField
              label="Add Popular Location"
              value={popularLocation}
              onChange={(e) => setPopularLocation(e.target.value)}
              fullWidth
              margin="normal"
            />
            <IconButton onClick={handleAddPopularLocation} color="primary">
              <AddCircleOutline />
            </IconButton>
            <Box sx={{ display: "flex", flexWrap: "wrap", mt: 1 }}>
              {formData.popular_locations.map((location, index) => (
                <Chip
                  key={index}
                  label={location}
                  onDelete={() => handleDeleteChip("popular_locations", index)}
                  sx={{ margin: "5px" }}
                />
              ))}
            </Box>
          </Box>

          <TextField
            label="Target Market"
            name="target_market"
            value={formData.target_market}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="secondary">
          Cancel
        </Button>
        <Button onClick={handleSave} color="primary" variant="contained">
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CreateCompanyModal;

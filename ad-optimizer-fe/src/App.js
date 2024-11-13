// src/App.js
import React, { useState } from "react";
import { Container, CssBaseline, ThemeProvider, Box } from "@mui/material";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import OptimizeAd from "./components/OptimizeAd";
import PreviousAds from "./components/PreviousAds";
import CreatePropertyModal from "./components/CreatePropertyModal";
import CreateCompanyModal from "./components/CreateCompanyModal";
import theme from "./theme";
import { CompanyProvider } from "./context/CompanyContext"; // Import the context provider
import axios from "axios";

const App = () => {
  axios.defaults.baseURL = "http://127.0.0.1:5000"; // Set your base URL here
  const [isCreatePropertyModalOpen, setCreatePropertyModalOpen] =
    useState(false);
  const [isCreateCompanyModalOpen, setCreateCompanyModalOpen] = useState(false);

  const openCreateCompanyModal = () => setCreateCompanyModalOpen(true);
  const closeCreateCompanyModal = () => setCreateCompanyModalOpen(false);

  const openCreatePropertyModal = () => setCreatePropertyModalOpen(true);
  const closeCreatePropertyModal = () => setCreatePropertyModalOpen(false);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <CompanyProvider>
        <Router>
          <Header />
          <Box
            sx={{
              display: "flex",
              flexDirection: "row",
              minHeight: "100vh",
            }}
          >
            <Sidebar
              onCreateCompany={openCreateCompanyModal}
              onCreateProperty={openCreatePropertyModal}
            />
            <Container
              sx={{
                flexGrow: 1,
                marginTop: 8,
                paddingLeft: { xs: 0, md: 2 },
                paddingRight: { xs: 0, md: 2 },
              }}
            >
              <Routes>
                <Route path="/" element={<PreviousAds />} />
                <Route path="/optimize-ad" element={<OptimizeAd />} />
              </Routes>
            </Container>
          </Box>
          <CreatePropertyModal
            open={isCreatePropertyModalOpen}
            onClose={closeCreatePropertyModal}
          />
          <CreateCompanyModal
            open={isCreateCompanyModalOpen}
            onClose={closeCreateCompanyModal}
          />
        </Router>
      </CompanyProvider>
    </ThemeProvider>
  );
};

export default App;

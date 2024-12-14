import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";
import { BackendURL } from "./component/backendURL";

import { Home } from "./pages/home";
import { Demo } from "./pages/demo";
import { Single } from "./pages/single";
import injectContext from "./store/appContext";

import Navbar from "./component/navbar";
import Sidebar from "./component/sidebar"; // Corrected the import to use "sidebar"
import { Footer } from "./component/footer";

import Products from "./pages/products"; // Add corresponding page components
import Orders from "./pages/orders";
import TShirtDesign from "./pages/tshirtDesign";
import BookDesign from "./pages/bookDesign";
import Pricing from "./pages/pricing";
import Customers from "./pages/customers";
import Analytics from "./pages/analytics";
import Settings from "./pages/settings";

//create your first component
const Layout = () => {
  const basename = process.env.BASENAME || "";

  if (!process.env.BACKEND_URL || process.env.BACKEND_URL === "") return <BackendURL />;

  return (
    <div className="d-flex" style={{ height: "100vh" }}>
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex-grow-1" style={{ overflow: "auto" }}>
        <BrowserRouter basename={basename}>
          <ScrollToTop>
            <Navbar />
            <div className="container-fluid">
              <Routes>
                <Route element={<Home />} path="/" />
                <Route element={<Demo />} path="/demo" />
                <Route element={<Single />} path="/single/:theid" />
                <Route element={<Products />} path="/products" />
                <Route element={<Orders />} path="/orders" />
                <Route element={<TShirtDesign />} path="/tshirt-design" />
                <Route element={<BookDesign />} path="/book-design" />
                <Route element={<Pricing />} path="/pricing" />
                <Route element={<Customers />} path="/customers" />
                <Route element={<Analytics />} path="/analytics" />
                <Route element={<Settings />} path="/settings" />
                <Route element={<h1>Not found!</h1>} path="*" />
              </Routes>
            </div>
            <Footer />
          </ScrollToTop>
        </BrowserRouter>
      </div>
    </div>
  );
};

export default injectContext(Layout);

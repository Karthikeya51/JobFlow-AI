import React, { createContext, useState, useEffect } from "react";
import api from "../services/api";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Restore session on mount
  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }

    setIsLoading(false);
  }, []);

  const register = async (name, email, password) => {
    try {
      setError(null);
      const response = await api.post("/api/auth/register", {
        name,
        email,
        password,
      });
      return response.data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || "Registration failed";
      setError(errorMsg);
      throw err;
    }
  };

  const login = async (email, password) => {
    try {
      setError(null);
      const response = await api.post("/api/auth/login", {
        email,
        password,
      });

      const { access_token, user: userData } = response.data;

      setToken(access_token);
      setUser(userData);

      localStorage.setItem("token", access_token);
      localStorage.setItem("user", JSON.stringify(userData));

      return response.data;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || "Login failed";
      setError(errorMsg);
      throw err;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  };

  const value = {
    user,
    token,
    isLoading,
    error,
    isAuthenticated: !!token,
    register,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

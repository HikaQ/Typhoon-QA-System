export function getCurrentUser() {
  try {
    return JSON.parse(localStorage.getItem("currentUser") || "null");
  } catch (e) {
    return null;
  }
}

export function getAuthToken() {
  return localStorage.getItem("authToken");
}

export function saveAuth(authData) {
  if (!authData) return;
  if (authData.token) {
    localStorage.setItem("authToken", authData.token);
  }
  if (authData.user) {
    localStorage.setItem("currentUser", JSON.stringify(authData.user));
    localStorage.setItem("userRole", authData.user.type || "");
  }
}

export function clearAuth() {
  localStorage.removeItem("authToken");
  localStorage.removeItem("currentUser");
  localStorage.removeItem("userRole");
}

export function isAuthenticated() {
  return !!(getAuthToken() && getCurrentUser());
}

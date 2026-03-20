const USERS_KEY = "users";
const SESSION_KEY = "session";

function readJson(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch (error) {
    console.warn(`Failed to parse ${key}`, error);
    return fallback;
  }
}

function getUsers() {
  return readJson(USERS_KEY, []);
}

function saveUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
}

function setSession(user) {
  const sessionUser = {
    name: user.name || user.email || "User",
    email: user.email || "",
    role: user.role || "guest",
    provider: user.provider || "local"
  };

  localStorage.setItem(SESSION_KEY, JSON.stringify(sessionUser));
}

function getSession() {
  return readJson(SESSION_KEY, null);
}

async function hashPassword(password) {
  // For simplicity, return password as is (in production, use proper hashing)
  return password;
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function logout() {
  localStorage.removeItem(SESSION_KEY);
  window.location.href = "login.html";
}

async function register() {
  try {
    const name = document.getElementById("name")?.value.trim();
    const email = document.getElementById("email")?.value.trim().toLowerCase();
    const password = document.getElementById("password")?.value || "";
    const roleEl = document.querySelector('input[name="role"]:checked');

    if (!name || !email || !password || !roleEl) {
      alert("All fields are required.");
      return;
    }

    if (!isValidEmail(email)) {
      alert("Please enter a valid email address.");
      return;
    }

    if (password.length < 6) {
      alert("Password must be at least 6 characters.");
      return;
    }

    const users = getUsers();
    if (users.some((user) => user.email === email)) {
      alert("Email already registered.");
      return;
    }

    const passwordHash = await hashPassword(password);
    users.push({
      name,
      email,
      passwordHash,
      role: roleEl.value,
      provider: "local",
      createdAt: Date.now()
    });

    saveUsers(users);
    alert("Registered successfully.");
    window.location.replace("login.html");
  } catch (error) {
    console.error("Registration failed:", error);
    alert("An error occurred during registration. Please try again.");
  }
}

async function login() {
  try {
    const email = document.getElementById("email")?.value.trim().toLowerCase();
    const password = document.getElementById("password")?.value || "";

    if (!email || !password) {
      alert("Enter your email and password.");
      return;
    }

    const users = getUsers();
    const userByEmail = users.find((entry) => entry.email === email);

    if (!userByEmail) {
      alert("No account found with this email. Please register first.");
      return;
    }

    const passwordHash = await hashPassword(password);
    if (userByEmail.passwordHash !== passwordHash) {
      alert("Invalid credentials. Please check your email and password.");
      return;
    }

    // Candidate-specific access can be added by requiring a role.
    // Allow any valid registered role. Company and college users are now permitted too.
    const allowedRoles = ["student", "company", "college", "candidate", "admin", "guest"];
    if (userByEmail.role && !allowedRoles.includes(userByEmail.role)) {
      alert("Invalid role: your account role is not allowed.");
      return;
    }

    setSession(userByEmail);
    console.log("Login successful for:", userByEmail.email);
    window.location.href = "Event.html";
  } catch (error) {
    console.error("Login failed:", error);
    alert("An error occurred during login. Please try again.");
  }
}

function resetPassword() {
  const emailInput = document.getElementById("email");
  const newPasswordInput = document.getElementById("newPassword");
  const confirmPasswordInput = document.getElementById("confirmPassword");

  const email = emailInput?.value.trim().toLowerCase();
  const newPassword = newPasswordInput?.value || "";
  const confirmPassword = confirmPasswordInput?.value || "";

  if (!email || !newPassword || !confirmPassword) {
    alert("Please fill in all fields.");
    return Promise.resolve();
  }

  if (!isValidEmail(email)) {
    alert("Please enter a valid email address.");
    return Promise.resolve();
  }

  if (newPassword.length < 6) {
    alert("New password must be at least 6 characters.");
    return Promise.resolve();
  }

  if (newPassword !== confirmPassword) {
    alert("Passwords do not match.");
    return Promise.resolve();
  }

  return hashPassword(newPassword).then((passwordHash) => {
    const users = getUsers();
    const index = users.findIndex((user) => user.email === email);

    if (index === -1) {
      alert("No account found with that email.");
      return;
    }

    users[index].passwordHash = passwordHash;
    saveUsers(users);

    alert("Password reset successfully. You can now log in.");
    window.location.href = "login.html";
  });
}

function requireAuth(requiredRole = null) {
  const session = getSession();
  if (!session) {
    window.location.href = "login.html";
    return;
  }

  if (requiredRole && session.role !== requiredRole) {
    alert("Access denied: invalid candidate role.");
    logout();
  }
}

// Social Login Mocks
function loginWithGoogle() {
  const users = getUsers();
  const mockUser = {
    name: "Google User",
    email: "user@gmail.com",
    role: "student",
    provider: "google",
    createdAt: Date.now()
  };

  // Persist Google user for future session checks
  if (!users.some((u) => u.email === mockUser.email)) {
    users.push(mockUser);
    saveUsers(users);
  }

  setSession(mockUser);
  window.location.href = "Event.html";
}

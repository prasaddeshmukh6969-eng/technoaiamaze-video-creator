import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface User {
    id: string;
    email: string;
    phone: string;
    created_at: string;
}

interface AuthState {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;
}

export function useAuth() {
    const [authState, setAuthState] = useState<AuthState>({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: true
    });

    useEffect(() => {
        // Check for existing token on mount
        const token = localStorage.getItem('auth_token');
        const userStr = localStorage.getItem('auth_user');

        if (token && userStr) {
            try {
                const user = JSON.parse(userStr);
                setAuthState({
                    user,
                    token,
                    isAuthenticated: true,
                    isLoading: false
                });
            } catch (error) {
                localStorage.removeItem('auth_token');
                localStorage.removeItem('auth_user');
                setAuthState({ user: null, token: null, isAuthenticated: false, isLoading: false });
            }
        } else {
            setAuthState({ user: null, token: null, isAuthenticated: false, isLoading: false });
        }
    }, []);

    const register = async (email: string, phone: string, password: string) => {
        try {
            const response = await axios.post(`${API_URL}/api/v1/auth/register`, {
                email,
                phone,
                password
            });

            const { access_token, user } = response.data;

            localStorage.setItem('auth_token', access_token);
            localStorage.setItem('auth_user', JSON.stringify(user));

            setAuthState({
                user,
                token: access_token,
                isAuthenticated: true,
                isLoading: false
            });

            return { success: true };
        } catch (error: any) {
            return {
                success: false,
                error: error.response?.data?.detail || 'Registration failed'
            };
        }
    };

    const login = async (email: string, password: string) => {
        try {
            const response = await axios.post(`${API_URL}/api/v1/auth/login`, {
                email,
                password
            });

            const { access_token, user } = response.data;

            localStorage.setItem('auth_token', access_token);
            localStorage.setItem('auth_user', JSON.stringify(user));

            setAuthState({
                user,
                token: access_token,
                isAuthenticated: true,
                isLoading: false
            });

            return { success: true };
        } catch (error: any) {
            return {
                success: false,
                error: error.response?.data?.detail || 'Login failed'
            };
        }
    };

    const logout = () => {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
        setAuthState({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false
        });
    };

    return {
        ...authState,
        register,
        login,
        logout
    };
}

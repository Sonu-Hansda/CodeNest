import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

interface Attempt {
    id: number;
    problem_title: string;
    passed: boolean;
    created_at: string;
  }
  
  interface User {
    id: number;
    username: string;
    email: string;
    score: number;
    attempts: Attempt[];
  }
  
export default function Profile(){
    
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const {token} = useAuth();

    useEffect(() => {
        const fetchProfile = async () => {
          try {
            const response = await api.get(`/account/profile`, {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            });
            setUser(response.data);
          } catch (error) {
            toast.error('Error fetching profile');
          } finally {
            setLoading(false);
          }
        };
    
        fetchProfile();
      }, []);

      if (loading) {
        return <div>Loading...</div>;
      }
    
      if (!user) {
        return <div>No user data available</div>;
      }

      
    return (
        <div className="container mx-auto py-6 px-24">
      <div className="bg-white shadow-md rounded-lg p-4 mb-6">
        <h1 className="text-3xl font-bold mb-4">Profile</h1>
        <div className="mb-4">
          <h2 className="text-xl font-bold">User Information</h2>
          <p><strong>Username:</strong> {user.username}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Score:</strong> {user.score}</p>
        </div>
        <div className="mb-4">
          <h2 className="text-xl font-bold">Recent Attempts</h2>
          <ul className="space-y-4">
            {user.attempts.map(attempt => (
              <li key={attempt.id} className={`p-4 rounded-lg shadow-md ${attempt.passed ? 'bg-green-100' : 'bg-red-100'}`}>
                <p className="text-lg font-semibold"><strong>Problem:</strong> {attempt.problem_title}</p>
                <p className="text-lg"><strong>Passed:</strong> {attempt.passed ? 'Yes' : 'No'}</p>
                <p className="text-lg"><strong>Date:</strong> {new Date(attempt.created_at).toLocaleString()}</p>
              </li>
            ))}
          </ul>
        </div>
        <div className="flex space-x-4">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Change Password
          </button>
          <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
            Edit Profile
          </button>
        </div>
      </div>
    </div>
    );
}
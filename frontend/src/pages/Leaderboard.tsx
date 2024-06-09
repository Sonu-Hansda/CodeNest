import { useEffect, useState } from "react";
import api from "../services/api";
import { toast } from "react-toastify";

interface User {
    id: number;
    username: string;
    email: string;
    score: number;
  }

export default function Leaderboard(){
    const [users,setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchLeaderboard = async () => {
        try {
        const response = await api.get('/leaderboard');
        setUsers(response.data);
      } catch (error) {
        toast.error('Error fetching leaderboard');
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }
    return (
        <div className="container mx-auto py-6 px-24">
          <h1 className="text-3xl font-bold mb-4">Leaderboard</h1>
          <table className="min-w-full bg-white border border-gray-300">
            <thead>
              <tr>
                <th className="py-2 px-4 border-b">#Rank</th>
                <th className="py-2 px-4 border-b">Username</th>
                <th className="py-2 px-4 border-b">Email</th>
                <th className="py-2 px-4 border-b">Score</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user, index) => (
                <tr key={user.id} className={(index+1) % 2 == 0 ? 'bg-gray-200': ''}>
                  <td className="py-2 px-4 border-b text-center">{index + 1}</td>
                  <td className="py-2 px-4 border-b">{user.username}</td>
                  <td className="py-2 px-4 border-b">{user.email}</td>
                  <td className="py-2 px-4 border-b text-center">{user.score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
}
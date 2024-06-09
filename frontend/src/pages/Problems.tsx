import { useState, useEffect } from "react";
import api from "../services/api";
import IProblem from "../interfaces/Problem";
import { Link } from "react-router-dom";

export default function Problems (){
 const [problems, setProblems] = useState<IProblem[]>([]);

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        const response = await api.get('http://localhost:8000/api/problems/getAll');
        setProblems(response.data);
      } catch (error) {
        console.error('Error fetching problems:', error);
      }
    };

    fetchProblems();
  }, []);
    return (
        <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4">All Problems</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {problems.map(problem => (
          <div key={problem.id} className="bg-white shadow-md rounded-lg p-4">
            <h2 className="text-xl font-bold mb-2">{problem.title}</h2>
            <p className="mb-4">{problem.description}</p>
            <div className="flex justify-end">
            <Link to={"/problems/"+problem.id}>
              <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
                View Problem
              </button>
            </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
    );
}
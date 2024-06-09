import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

interface TestCase {
  input: string;
  expected_output: string;
}

interface Problem {
  title: string;
  description: string;
  code: string;
  point: number;
  test_cases: TestCase[];
}

const AddProblem: React.FC = () => {
  const [title, setTitle] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [code, setCode] = useState<string>('');
  const [point, setPoint] = useState<number>(0);
  const [testCases, setTestCases] = useState<TestCase[]>([{ input: '', expected_output: '' }]);
  const {token} = useAuth();
  const [loading,setLoading] = useState<boolean>(false);
  const handleAddTestCase = () => {
    setTestCases([...testCases, { input: '', expected_output: '' }]);
  };

  const handleRemoveTestCase = (index: number) => {
    const newTestCases = testCases.filter((_, i) => i !== index);
    setTestCases(newTestCases);
  };

  const handleTestCaseChange = (index: number, key: string, value: string) => {
    const newTestCases = testCases.map((testCase, i) =>
      i === index ? { ...testCase, [key]: value } : testCase
    );
    setTestCases(newTestCases);
  };

  const handleSubmit = async () => {
    // Check if title is present
    if (!title.trim()) {
      toast.error('Title is required');
      return;
    }
  
    // Check if at least one test case is present
    if (!testCases.length || !testCases[0].input.trim() || !testCases[0].expected_output.trim()) {
      toast.error('At least one test case is required');
      return;
    }
  
    const newProblem: Problem = {
      title,
      description,
      code,
      point,
      test_cases: testCases,
    };
  
    setLoading(true);
    
    try {
      const response = await api.post('/problems', newProblem, {
        headers: {
          Authorization: "Bearer "+`${token}`,
        },
      });
  
      console.log(response);
      
      if (response.status === 201) {
        toast.success('Problem added successfully');
        setTitle('');
        setDescription('');
        setCode('');
        setPoint(0);
        setTestCases([{ input: '', expected_output: '' }]);
      }
    } catch (error) {
      toast.error('Error adding problem');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6">
      <div className="bg-white shadow-md rounded-lg py-4 px-24 mb-6">
        <h1 className="text-3xl font-bold mb-4">Add New Problem</h1>

        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">Title</label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">Description</label>
          <textarea
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">Code</label>
          <textarea
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            value={code}
            placeholder='Initial Code'
            onChange={(e) => setCode(e.target.value)}
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">Points</label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            type="number"
            value={point}
            onChange={(e) => setPoint(Number(e.target.value))}
          />
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">Test Cases</label>
          {testCases.map((testCase, index) => (
            <div key={index} className="mb-4">
              <div className="flex">
                <input
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mr-2"
                  type="text"
                  placeholder="Input"
                  value={testCase.input}
                  onChange={(e) => handleTestCaseChange(index, 'input', e.target.value)}
                />
                <input
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  type="text"
                  placeholder="Expected Output"
                  value={testCase.expected_output}
                  onChange={(e) => handleTestCaseChange(index, 'expected_output', e.target.value)}
                />
              </div>
              {testCases.length > 1 && (
                <button
                  className="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 mt-2 rounded focus:outline-none focus:shadow-outline"
                  onClick={() => handleRemoveTestCase(index)}
                >
                  Remove
                </button>
              )}
            </div>
          ))}
          <button
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            onClick={handleAddTestCase}
          >
            Add Test Case
          </button>
        </div>

         <div className="flex items-center justify-between">
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              disabled={loading}
              onClick={handleSubmit}
            >
              {loading ? (
                <svg className="animate-spin h-5 w-5 text-white mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
              ) : (
                "Submit"
              )}
            </button>
          </div>
      </div>
    </div>
  );
};

export default AddProblem;

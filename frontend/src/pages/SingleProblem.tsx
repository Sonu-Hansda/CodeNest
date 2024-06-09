import { useEffect, useState } from "react";
import IProblem from "../interfaces/Problem";
import { useParams } from "react-router-dom";
import api from "../services/api";
import CodeEditor from "../components/CodeEditor";
import { toast } from "react-toastify";
import { useAuth } from "../context/AuthContext";

export default function SingleProblem() {
    const [problem, setProblem] = useState<IProblem | null>(null);
    const { id } = useParams();
    const [language, setLanguage] = useState<string>("python");
    const [solutionCode, setSolutionCode] = useState<string>("");
    const [evaluating,setEvaluating] = useState<boolean>(false);
    const [results,setResults] = useState<any[]>([]);
    const {token} = useAuth();

    const handleCodeChange = (newValue: string) => {
        setSolutionCode(newValue);
    };

    const handleEvaluation = async () => {
        setEvaluating(true);
        try {
            const solution = {
                code: solutionCode,
                language: language,
                problem_code: parseInt(id ?? '0')
            };
            
            const response = await api.post('/problems/evaluate', solution, {
                headers: {
                  Authorization: 'Bearer '+token,
                },
              });

            if (response.status !== 200) {
                throw new Error(response.statusText);
            }
            setResults(response.data.test_cases);
            
        } catch (error) {
            console.error("Evaluation failed:", error);
            toast.error("Failed to evaluate code. Please try again.");
        } finally {
            setEvaluating(false);
        }
    };

    useEffect(() => {
        const fetchProblem = async () => {
            try {
                const response = await api.get('/problems/' + id);
                setProblem(response.data);
                setSolutionCode(problem ? problem.code : "");
            } catch (error) {
                console.error('Error fetching problems:', error);
            }
        };

        fetchProblem();
    }, []);

    if (!problem) {
        return <div>Loading...</div>;
    }

    return (
        <div className="container mx-auto py-6 px-24">
            <h1 className="text-3xl font-bold mb-4">{problem.title}</h1>
            <div className="bg-white shadow-md rounded-lg p-4 mb-6">
                <h2 className="text-xl font-bold mb-2">Description</h2>
                <p>{problem.description}</p>
            </div>
            <div className="bg-white shadow-md rounded-lg p-4">
                <h2 className="text-xl font-bold mb-2">Test Cases</h2>
                <ul>
                    {problem.test_cases.map((testCase: any, index: number) => (
                        <li key={index} className="mb-2">
                            <p>
                                <span className="font-bold">Input:</span> {testCase.input}
                            </p>
                            <p>
                                <span className="font-bold">Expected Output:</span>{' '}
                                {testCase.expected_output}
                            </p>
                        </li>
                    ))}
                </ul>
            </div>
            <div className="bg-white shadow-md rounded-lg p-4">
                <div className="flex justify-between">
                    <h2 className="text-xl font-bold mb-2">Solution Code</h2>
                    <select
                        name="language"
                        id="language"
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="bg-white rounded-md border border-gray-300 px-3 py-2 mb-2"
                    >
                        <option value="python">Python</option>
                        <option value="c">C</option>
                        <option value="cpp">C++</option>
                    </select>
                </div>
                <CodeEditor
                    language={language}
                    defaultValue={solutionCode}
                    onChange={handleCodeChange}
                />
                <button
                    onClick={handleEvaluation}
                    className={`bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 my-2 rounded focus:outline-none focus:shadow-outline ${
                        evaluating ? 'opacity-50 cursor-not-allowed' : ''
                    }`}
                    disabled={evaluating}
                >
                    {evaluating ? 'Evaluating...' : 'Evaluate'}
                </button>
            </div>
            <div className="bg-white shadow-md rounded-lg p-4 mt-6">
                <h2 className="text-xl font-bold mb-2">Evaluation Results</h2>
                {results.length > 0 ? (
                    results.map((result, index) => (
                        <div key={index} className="border-b border-gray-300 pb-2 mb-2">
                            <p>
                                <span className="font-bold">Input:</span> {result.input}
                            </p>
                            <p>
                                <span className="font-bold">Expected Output:</span> {result.expected_output}
                            </p>
                            <p>
                                <span className="font-bold">Actual Output:</span> {result.actual_output}
                            </p>
                            {result.passed ? (
                                <p className="text-green-600 font-bold">Passed</p>
                            ) : (
                                <p className="text-red-600 font-bold">Failed</p>
                            )}
                            <p>
                                <span className="font-bold">Time Taken:</span> {result.time_taken} seconds
                            </p>
                        </div>
                    ))
                ) : (
                    <p>No evaluation results available.</p>
                )}
            </div>
        </div>
    );
};
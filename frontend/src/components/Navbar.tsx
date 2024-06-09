import { Link } from "react-router-dom"
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
    const { token, logout } = useAuth();
    return (
        <nav className="bg-blue-600 py-4 px-24 text-white shadow-lg">
            <div className="container mx-auto flex justify-between items-center">
                <Link to={"/"}>
                    <h1 className="text-2xl font-bold">CodeNest</h1>
                </Link>
                <ul className="flex space-x-4">
                    <Link to={"/leaderboard"}>
                    <li className="hover:underline">Leaderboard</li>
                    </Link>
                    <Link to={"/problems/all"}>
                    <li className="hover:underline">Problems</li>
                    </Link>
                    {token == null ? (
                        <>
                        <Link to={"/log-in"}>
                            <li className="hover:underline">Sign In</li>
                        </Link>
                        <Link to={"/register"}>
                            <li className="hover:underline">Register</li>
                        </Link>
                        </>
                    ) : (
                        <>
                        <Link to={"/problems/add"}>
                            <li className="hover:underline">Add Problem</li>
                        </Link>
                        <Link to={"/profile"}>
                            <li className="hover:underline">Profile</li>
                        </Link>
                            <li onClick={logout} className="cursor-pointer hover:underline">Log out</li>
                        </>
                    )}
                </ul>
            </div>
        </nav>
    );
}
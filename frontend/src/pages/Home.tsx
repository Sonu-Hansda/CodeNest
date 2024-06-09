export default function Home(){
    return (
        <>
         <section id="introduction" className="py-20 px-24 bg-gray-100">
      <div className="container mx-auto text-center">
        <h2 className="text-3xl font-bold mb-4">Welcome to CodeNest</h2>
        <p className="text-lg">
          CodeNest is a platform where you can solve coding problems and improve your programming skills. 
          Whether you're a beginner or an experienced developer, you'll find challenges that match your level.
        </p>
      </div>
    </section>
    <section id="how-it-works" className="py-20 px-24">
      <div className="container mx-auto text-center">
        <h2 className="text-3xl font-bold mb-4">How It Works</h2>
        <p className="text-lg mb-4">
          At CodeNest, we support multiple programming languages including C, Python, and C++. 
          Simply select a problem, write your solution, and submit it to see if it passes all test cases.
        </p>
        <div className="flex justify-center space-x-4">
          <span className="bg-gray-200 px-4 py-2 rounded">C</span>
          <span className="bg-gray-200 px-4 py-2 rounded">Python</span>
          <span className="bg-gray-200 px-4 py-2 rounded">C++</span>
        </div>
      </div>
    </section>
    </>
    );
}
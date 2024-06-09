export default interface IProblem {
    id: number;
    title: string;
    description: string;
    author: {
      id: number;
      username: string;
      email: string;
    };
    code: string;
    test_cases: {
      input: string;
      expected_output: string;
    }[];
  }
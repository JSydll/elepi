"""
verification.py

This module provides a Verification class that offers methods to verify solutions to quests.
It includes functionality to convert solution code to a signature and to verify the signature
against a provided verification key and solution token.

"""
import subprocess


class Verification:
    """
    Provides a simple interface for verifying solutions to quests.
    """

    @staticmethod
    def get_signature(solution_code: str) -> bytes:
        """
        Converts the solution code to a signature.

        Args:
            solution_code: A hex code representing the solution signature.

        Returns:
            bytes: The signature.
        """

        result = subprocess.run(
            ["xxd", "-r", "-p"],
            input=solution_code.encode(),
            capture_output=True,
            check=True,
            text=False
        )

        return result.stdout

    @staticmethod
    def check_signature(signature: bytes, key_path: str, token_path: str) -> bool:
        """
        Verifies the provided signature against the quest's verification key.

        Args:
            signature: The signature to verify.
            key_path: The path to the verification key.
            token_path: The path to the solution token.

        Returns:
            bool: True if the signature is verified successfully, false otherwise.
        """

        result = subprocess.run(
            [
                "openssl", "dgst", "-sha512", "-verify", key_path,
                "-signature", "/dev/stdin", token_path
            ],
            input=signature,
            capture_output=True,
            text=False
        )

        return result.returncode == 0

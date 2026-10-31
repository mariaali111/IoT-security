# Implementation of ECC-LRE, Steganographic IoT Security Protocol

## Security Notes
- This is a research / educational implementation. Do not use it for production high-security scenarios without thorough review and additional hardening.
- ECC provides strong confidentiality; the steganographic layer aims for undetectability under standard statistical attacks.
- Always use authenticated encryption (or signcryption) and protect private keys.
- Channel noise and lossy recompression can introduce bit errors; enable the optional forward-error-correction layer when operating over social media or lossy links.

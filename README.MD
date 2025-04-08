# Explorations of PRNG

## CPSC 418 - Group 7 Final Project

Tests the quality of pseudo random numbers using the NIST SP800-22 testing suite. Also contains a theoretical attack against encryption keys generated using weak Linear Congruential Generation. 


## Table of Contents
- [Installation](#installation)
- [Usage](#usage)


## Installation

## Usage

#### Attack Demonstration
The entry point to the simulation is within [Showcase](attack_demonstration/showcase.py). For control over the simulation adjust the following parameters:
- lcg_range | This parameter controls the range of the initial seeding for the victims LCG. In theory this would always be at 31 (which represents 2^31 bits of range) but in practice it can be lower. A lower range will allow the brute forcing to find the key faster. You can keep it at 31 but this will result in ~2.5 hours of computation.
- max_cores | Ideally this should be equal to the core count of your CPU however it can be lower. Be warned that this can eat your entire CPU.

#### Randomness Testing


# Solutions to DART exercise

- Q1: Is a scene/landscape Lambertian if all scene elements are Lambertian?

A1: No. Lambertian reflection requires the whole scene to be isotropic, meaning it uniformly reflects light in all directions. However, in real-world scenarios, shadows, shading, and multiple scattering disrupt this isotropy.

- Q2: In the nadir image, a roof slope has a reflectance equal to 0.54 and the other one has a reflectance equal to 0.39 even though the 2 slopes are made of a same material with reflectance = 0.5. Why? Give the analytical equation of the observed reflectance of the slopes?

A2: The difference between the two slopes stems from the solar zenith angle. The left side is illuminated more than the right side. From the character data, the left side's normal vector is $\overrightarrow{\Omega_{lslope}}=\dfrac{1}{\sqrt{29}}(0,-2,5)$, while the right side's normal vector is $\overrightarrow{\Omega_{rslope}}=\dfrac{1}{\sqrt{29}}(0,2,5)$. Given that SZA = 30° and SAA = 225°, we can get $\overrightarrow{\Omega_s}=(-\dfrac{\sqrt{2}}{4},-\dfrac{\sqrt{2}}{4},\dfrac{\sqrt{3}}{2})$  
according to the equation 
$$\rho_{1,\text{slope}}^* = \rho_{\text{slope}} \cdot \frac{\overline{\Omega}_{\text{s}} \cdot \overline{\Omega}_{\text{slope}}}{\overline{\Omega}_{\text{s}} \cdot \overline{\Omega}_{\text{ground}}} = \rho_{\text{slope}} \cdot \frac{E_{\text{slope}}}{E_{\text{BOA}}}$$ 
the left side's observed reflectance = $0.5 \times \dfrac{\sqrt{2}+5\sqrt{3}}{\sqrt{29} \times \sqrt{3}} \approx 0.54$ (handle the overall +/- sign manually)  
For the same reason, the right side's observed reflectance = $0.5 \times \dfrac{-\sqrt{2}+5\sqrt{3}}{\sqrt{29} \times \sqrt{3}} \approx 0.39$  


- Q3: Here: $\rho_{scene}=0.462$ at nadir. With the help of DART simulations, answer the 2 questions:
  - 3.1 Does $\rho_{scene}=0.462$ increase or decrease if SZA increases?
  - 3.2 For which SZA, while keeping SAA=225°, do we get $\rho_{scene}=0.238$ and $\rho_{scene}=0.501$?


A3.1:   
When the SZA increased from 30° to 80°, the reflectance decreased from 0.462 to 0.238.

| SZA/° | reflectance |
|-----|-------------|
| 30 | 0.462 |
| 40 | 0.445 |
| 50 | 0.421 |
| 60 | 0.385 |
| 70 | 0.319 |
| 80 | 0.238 |

A3.2:   
I'm not sure whether the reflectance can reach to 238. Anyway, if the number is 0.238, then SZA = 80°; when SZA = 0°, the reflectance = 0.501.

**Thank you for your insightful and inspiring lectures. I sincerely appreciate the opportunity to learn from your expertise.**  

*As English is not my native language, please accept my apologies for any unintended errors in my submission.*
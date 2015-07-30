uniform vec3 rangeMin;
uniform vec3 rangeMax;

out vec4 fragColor;
void main()
{
	vec3 pos = texture(sTD2DInputs[0], vUV.st).rgb;
	pos = mix(rangeMin, rangeMax, pos);
	pos.z += uTD3DInfos[0].depth.z;
	vec4 color = texture(sTD3DInputs[0], pos);
	fragColor = color;
}

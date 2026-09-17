// Original procedural rock; world-space centimetres. No external texture dependencies.
struct RockNoise {
 float hash(float3 p) {p=frac(p*.1031);p+=dot(p,p.yzx+33.33);return frac((p.x+p.y)*p.z);}
 float noise(float3 p) {float3 i=floor(p),f=frac(p);f=f*f*(3-2*f);return lerp(lerp(lerp(hash(i),hash(i+float3(1,0,0)),f.x),lerp(hash(i+float3(0,1,0)),hash(i+float3(1,1,0)),f.x),f.y),lerp(lerp(hash(i+float3(0,0,1)),hash(i+float3(1,0,1)),f.x),lerp(hash(i+float3(0,1,1)),hash(i+1),f.x),f.y),f.z);}
 float fbm(float3 p) {float v=0,a=.5;[unroll]for(int i=0;i<4;i++){v+=a*noise(p);p=p*2.03+float3(17.1,9.2,13.7);a*=.5;}return v;}
};
RockNoise r;
float3 p=P/max(Scale,0.01);
float macro=r.fbm(p*.0016);
float grain=r.fbm(p*.055);
float body=r.fbm(p*.009+macro*3);
float vein=abs(r.noise(p*.004+body*1.5)-.5);
float fissure=1-smoothstep(.012,.06,vein);
float oxide=smoothstep(.36,.65,macro+body*.16);
float3 color=lerp(Grey,Red,saturate(oxide*RedAmount));
color*=.65+body*.55+grain*.35;
color*=1-fissure*.38;
float quartz=pow(saturate(grain*1.6),10)*.12;
color+=quartz*float3(.65,.61,.56);
float height=body*2.6+grain*.5-fissure*.75;
return float4(color,height);

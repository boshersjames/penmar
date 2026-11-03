// Penmar -> Build Chain-Link Fence
// Builds a galvanised chain-link fence (steel posts, top rail, see-through diamond mesh) from a fences.csv
// (segment,x,z,y; Unity frame). Posts sit on the terrain, so the csv y is only a fallback.
// Solid colliders everywhere (BoJa: balls must never pass through nets or fences): mesh GSPtimber, posts and rail GSPconcrete.
// Unity 2018.2 / GSP base project. Copy to Assets/Editor/.
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using UnityEditor;
using UnityEngine;

public class ChainLinkFence : EditorWindow
{
    string csvPath = "Assets/Penmar/fences.csv";
    float height = 3.66f;          // 12 ft (Penmar perimeter)
    float postSpacing = 3.0f;      // line posts every 10 ft
    float postDiameter = 0.06f;
    float railDiameter = 0.042f;
    bool midRail = true;           // second rail at half height, as on the Penmar fence
    float diamond = 0.06f;         // 2 3/8 in mesh, one texture tile = 1 diamond
    Color wire = new Color(0.62f, 0.64f, 0.63f, 1f);
    float wireWidth = 0.12f;       // share of a diamond that is wire

    [MenuItem("Penmar/Build Chain-Link Fence")]
    static void Open() { GetWindow<ChainLinkFence>("Chain-Link Fence"); }

    void OnGUI()
    {
        csvPath = EditorGUILayout.TextField("fences.csv", csvPath);
        height = EditorGUILayout.FloatField("Height (m)", height);
        postSpacing = EditorGUILayout.FloatField("Post spacing (m)", postSpacing);
        postDiameter = EditorGUILayout.FloatField("Post diameter (m)", postDiameter);
        railDiameter = EditorGUILayout.FloatField("Top rail diameter (m)", railDiameter);
        midRail = EditorGUILayout.Toggle("Mid rail", midRail);
        diamond = EditorGUILayout.FloatField("Mesh diamond (m)", diamond);
        wireWidth = EditorGUILayout.Slider("Wire thickness", wireWidth, 0.04f, 0.3f);
        wire = EditorGUILayout.ColorField("Wire colour", wire);
        if (GUILayout.Button("Build")) Build();
    }

    void Build()
    {
        if (!File.Exists(csvPath)) { EditorUtility.DisplayDialog("Chain-Link Fence", "No file at " + csvPath, "OK"); return; }
        var segs = new SortedDictionary<int, List<Vector3>>();
        foreach (var line in File.ReadAllLines(csvPath))
        {
            var p = line.Split(',');
            int s;
            if (p.Length < 4 || !int.TryParse(p[0], out s)) continue;
            float x = float.Parse(p[1], CultureInfo.InvariantCulture), z = float.Parse(p[2], CultureInfo.InvariantCulture), y = float.Parse(p[3], CultureInfo.InvariantCulture);
            if (!segs.ContainsKey(s)) segs[s] = new List<Vector3>();
            segs[s].Add(new Vector3(x, y, z));
        }

        var old = GameObject.Find("CHAINLINK_FENCES");
        if (old) DestroyImmediate(old);
        var root = new GameObject("CHAINLINK_FENCES");
        var meshMat = MeshMaterial();
        var steel = new Material(Shader.Find("Standard")) { color = wire };
        steel.SetFloat("_Metallic", 0.6f); steel.SetFloat("_Glossiness", 0.35f);
        AssetDatabase.CreateAsset(steel, "Assets/Penmar/ChainLinkSteel.mat");
        var leaves = Resources.Load<PhysicMaterial>("Physics/GSPtimber");   // solid, deadens the ball
        var concrete = Resources.Load<PhysicMaterial>("Physics/GSPconcrete");
        var t = Terrain.activeTerrain;

        foreach (var kv in segs)
        {
            var seg = new GameObject("Fence_" + kv.Key);
            seg.transform.parent = root.transform;
            var posts = Resample(kv.Value, postSpacing);
            for (int i = 0; i < posts.Count; i++)
                if (t) posts[i] = new Vector3(posts[i].x, t.SampleHeight(posts[i]) + t.transform.position.y, posts[i].z);

            // mesh panels, split so no mesh passes 65k vertices
            var verts = new List<Vector3>(); var uvs = new List<Vector2>(); var tris = new List<int>();
            float dist = 0; int chunk = 0;
            for (int i = 0; i + 1 < posts.Count; i++)
            {
                Vector3 a = posts[i], b = posts[i + 1];
                float len = Vector3.Distance(new Vector3(a.x, 0, a.z), new Vector3(b.x, 0, b.z));
                int v0 = verts.Count;
                verts.Add(a); verts.Add(b); verts.Add(b + Vector3.up * height); verts.Add(a + Vector3.up * height);
                uvs.Add(new Vector2(dist / diamond, 0)); uvs.Add(new Vector2((dist + len) / diamond, 0));
                uvs.Add(new Vector2((dist + len) / diamond, height / diamond)); uvs.Add(new Vector2(dist / diamond, height / diamond));
                tris.AddRange(new[] { v0, v0 + 2, v0 + 1, v0, v0 + 3, v0 + 2, v0, v0 + 1, v0 + 2, v0, v0 + 2, v0 + 3 });  // both faces
                dist += len;
                if (verts.Count > 60000) { MeshChunk(seg, chunk++, verts, uvs, tris, meshMat, leaves); verts.Clear(); uvs.Clear(); tris.Clear(); }

                // top rail
                var rail = Cylinder(seg.transform, "Rail", (a + b) / 2 + Vector3.up * (height - railDiameter / 2), railDiameter, Vector3.Distance(a, b), steel, concrete);
                rail.transform.rotation = Quaternion.FromToRotation(Vector3.up, (b - a).normalized);
                if (midRail)
                {
                    var mid = Cylinder(seg.transform, "MidRail", (a + b) / 2 + Vector3.up * height / 2, railDiameter, Vector3.Distance(a, b), steel, concrete);
                    mid.transform.rotation = rail.transform.rotation;
                }
            }
            if (verts.Count > 0) MeshChunk(seg, chunk, verts, uvs, tris, meshMat, leaves);
            for (int i = 0; i < posts.Count; i++)
                Cylinder(seg.transform, "Post", posts[i] + Vector3.up * (height + 0.05f) / 2, postDiameter, height + 0.05f, steel, concrete);
        }
        GameObjectUtility.SetStaticEditorFlags(root, StaticEditorFlags.BatchingStatic | StaticEditorFlags.OccluderStatic | StaticEditorFlags.OccludeeStatic);
        foreach (Transform c in root.GetComponentsInChildren<Transform>())
            GameObjectUtility.SetStaticEditorFlags(c.gameObject, StaticEditorFlags.BatchingStatic);
        UnityEditor.SceneManagement.EditorSceneManager.MarkSceneDirty(root.scene);
        Debug.Log("Chain-link fence: " + segs.Count + " segments built under CHAINLINK_FENCES");
    }

    static List<Vector3> Resample(List<Vector3> pts, float step)
    {
        var o = new List<Vector3> { pts[0] };
        for (int i = 0; i + 1 < pts.Count; i++)
        {
            float L = Vector3.Distance(pts[i], pts[i + 1]);
            int n = Mathf.Max(1, Mathf.CeilToInt(L / step));
            for (int k = 1; k <= n; k++) o.Add(Vector3.Lerp(pts[i], pts[i + 1], k / (float)n));  // keeps every corner
        }
        return o;
    }

    static GameObject Cylinder(Transform parent, string name, Vector3 pos, float dia, float len, Material m, PhysicMaterial pm)
    {
        var g = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        g.name = name; g.transform.parent = parent; g.transform.position = pos;
        g.transform.localScale = new Vector3(dia, len / 2, dia);
        g.GetComponent<Renderer>().sharedMaterial = m;
        g.GetComponent<Collider>().sharedMaterial = pm;
        return g;
    }

    static void MeshChunk(GameObject seg, int k, List<Vector3> v, List<Vector2> uv, List<int> tri, Material m, PhysicMaterial pm)
    {
        var mesh = new Mesh { name = seg.name + "_mesh_" + k };
        mesh.SetVertices(v); mesh.SetUVs(0, uv); mesh.SetTriangles(tri, 0);
        mesh.RecalculateNormals(); mesh.RecalculateBounds();
        AssetDatabase.CreateAsset(mesh, "Assets/Penmar/" + mesh.name + ".asset");
        var g = new GameObject("Mesh_" + k);
        g.transform.parent = seg.transform;
        g.AddComponent<MeshFilter>().sharedMesh = mesh;
        g.AddComponent<MeshRenderer>().sharedMaterial = m;
        g.AddComponent<MeshCollider>().sharedMesh = mesh;
        g.GetComponent<MeshCollider>().sharedMaterial = pm;
    }

    Material MeshMaterial()
    {
        if (!AssetDatabase.IsValidFolder("Assets/Penmar")) AssetDatabase.CreateFolder("Assets", "Penmar");
        const int N = 64;
        var tex = new Texture2D(N, N, TextureFormat.RGBA32, true);
        float w = wireWidth * N / 2;
        for (int y = 0; y < N; y++)
            for (int x = 0; x < N; x++)
            {
                // two sets of diagonal wires = diamonds; distance to the nearest wire on either diagonal
                float d1 = Mathf.Abs(Mathf.Repeat(x + y, N) - N / 2f), d2 = Mathf.Abs(Mathf.Repeat(x - y, N) - N / 2f);
                float d = Mathf.Min(N / 2f - d1, N / 2f - d2);
                float a = Mathf.Clamp01(w - d + 0.5f);
                tex.SetPixel(x, y, new Color(wire.r, wire.g, wire.b, a));
            }
        tex.Apply();
        string png = "Assets/Penmar/ChainLink.png";
        File.WriteAllBytes(png, tex.EncodeToPNG());
        AssetDatabase.ImportAsset(png);
        var imp = (TextureImporter)AssetImporter.GetAtPath(png);
        imp.alphaIsTransparency = true; imp.wrapMode = TextureWrapMode.Repeat; imp.mipmapEnabled = true;
        imp.mipMapsPreserveCoverage = true; imp.alphaTestReferenceValue = 0.4f;   // keeps the mesh visible at a distance
        imp.SaveAndReimport();
        var m = new Material(Shader.Find("Standard"));
        m.mainTexture = AssetDatabase.LoadAssetAtPath<Texture2D>(png);
        m.SetFloat("_Mode", 1); m.SetFloat("_Cutoff", 0.4f);
        m.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.One); m.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.Zero);
        m.SetInt("_ZWrite", 1); m.EnableKeyword("_ALPHATEST_ON"); m.renderQueue = 2450;
        m.SetFloat("_Metallic", 0.5f); m.SetFloat("_Glossiness", 0.3f);
        m.SetInt("_Cull", 0);
        AssetDatabase.CreateAsset(m, "Assets/Penmar/ChainLinkMesh.mat");
        return m;
    }
}

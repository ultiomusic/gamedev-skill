# Synthetic specialist evaluation

This is a supplied reasoning fixture, not a running game or measured capture. No Unity project may be opened or changed. The user's request is: "Audit this small 3D collection game across rendering, feel, systems, and performance; give the smallest useful corrections and what would distinguish them. Keep the current calm pace and art style."

Target: mouse/keyboard desktop, intended 60 FPS, engine/version not supplied. Normal controls move with WASD, select with a click, then collect with E. The camera and controller are shared resources: the coordinator owns any edits. This is read-only. No profiler capture, rendered frame, or player study is available. Treat all supplied behavior as fixture evidence, not a live observation.

## Scene and fragments

```text
CollectorRoot at (0, 0, 0)
  VisibleOrb localPosition = (5, 0, 0), bobbing visual child
  SelectionMarker uses Camera.WorldToScreenPoint(CollectorRoot.position)

OnCollectPressed:
  if recoveryRemaining > 0:
    pendingPress = true
    Show("Not ready; command rejected")
    return
  StartCollect()

Update(dt):
  recoveryRemaining -= dt
  if recoveryRemaining <= 0 and pendingPress:
    pendingPress = false
    StartCollect()

OnCancel:
  HideCollectPreview()
  // pendingPress is unchanged

StartCollect:
  recoveryRemaining = 0.8
  AnimatePickupToInventory(amount = 8, onArrival = Finish)

Finish(pickup):
  accepted = min(pickup.amount, capacity - inventory)
  inventory += accepted
  Destroy(pickup)
  PlaySuccessSound(pickup.amount)
```

Source model for a boundary: inventory is 52, capacity 60 when collection starts; another transaction fills inventory to 60 before arrival. The intended rule says value that cannot fit stays collectible; cancellation must not trigger another action later. There is no reservation system.

The encounter adds 300 translucent decorative quads and creates/destroys them repeatedly. A developer reports "about 40 FPS in the Editor" and proposes pooling every object, disabling off-screen simulation, and removing sound. Navigation relies on directional sound; off-screen couriers carry rewards. No evidence establishes the hardware, CPU/GPU bottleneck, allocation rate, or retained memory.

Return only findings in your assigned specialist domain, necessary handoffs, and honest verification limits. Do not invent measurements, render observations, or implemented fixes.

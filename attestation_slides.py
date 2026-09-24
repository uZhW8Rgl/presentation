"""Editable slides for on-chain workload verification and dstack key derivation."""

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN


GREEN, PURPLE, BLUE = "207548", "7446A6", "1764A1"
INK, MUTED = "263440", "67747C"
TINT = {GREEN: "EDF6F0", PURPLE: "F3EEF8", BLUE: "EDF4FA"}


def _drawing(b, slide):
    def text(value, x, y, w, h=.3, size=14, color=INK, bold=False, center=True):
        shape = b.add_text(
            slide, value, x, y, w, h, size, color, bold,
            align=PP_ALIGN.CENTER if center else PP_ALIGN.LEFT,
            valign=MSO_ANCHOR.MIDDLE, margin=0,
        )
        shape.name = "Attestation: " + value.replace("\n", " / ")
        return shape

    def panel(x, y, w, h, color, fill=None):
        return b.add_box(slide, x, y, w, h, fill=fill or TINT[color],
                         line=color, line_width=1.1)

    def route(points, color=PURPLE, arrow=True, width=1.7):
        for index, (start, end) in enumerate(zip(points, points[1:])):
            b.add_line_segment(slide, *start, *end, color, width,
                               arrow=arrow and index == len(points) - 2)

    return text, panel, route


def verification(prs, b):
    slide = b.new_content_slide(
        prs, 14, "Verify the deployed worker image",
        "Submit app_compose, event log and TDX quote together for on-chain verification",
    )
    text, panel, route = _drawing(b, slide)

    text("WORKER TEE / DSTACK", .65, 1.55, 2.78, .30, 13, GREEN, True)
    panel(3.72, 1.48, 8.96, 4.73, PURPLE, "FAF8FC")
    text("ON CHAIN · DeviceRegistry + DCAP verifier", 3.98, 1.60, 8.40, .33,
         16, PURPLE, True)

    for y, h in [(2.10, .85), (3.50, .85), (4.90, 1.05)]:
        panel(.65, y, 2.78, h, GREEN)
        panel(3.98, y, 6.49, h, PURPLE, "FFFFFF")
        route([(3.47, y + h / 2), (3.94, y + h / 2)], GREEN)

    text("app_compose", .80, 2.20, 2.48, .31, 18, GREEN, True)
    text("…@sha256:Digest", .80, 2.61, 2.48, .23, 14)
    text("Compare image Digest with stored policy", 4.13, 2.20, 6.19, .31,
         17, PURPLE, True)
    text("DeviceRegistry.expectedWorkerImageDigest", 4.13, 2.62, 6.19, .23,
         13, INK)

    text("Event log", .80, 3.60, 2.48, .31, 18, GREEN, True)
    text("Ordered runtime events", .80, 4.01, 2.48, .23, 13)
    text("Replay the RTMR3 event chain", 4.13, 3.60, 6.19, .31,
         17, PURPLE, True)
    text("Start at zero · SHA-384 extend every event", 4.13, 4.01, 6.19, .23,
         13)

    text("TDX Quote", .80, 5.00, 2.48, .31, 18, GREEN, True)
    text("RTMR3 · REPORTDATA", .80, 5.49, 2.48, .25, 13)
    text("Verify quote authenticity and bindings", 4.13, 5.00, 6.19, .31,
         17, PURPLE, True)
    text("Intel signatures · TCB · base-runtime measurements\n"
         "REPORTDATA: participant · keys · nonce",
         4.13, 5.42, 6.19, .43, 12.5)

    # The compose preimage binds the image policy to the measured event log.
    route([(4.26, 2.99), (4.26, 3.46)], PURPLE)
    text("SHA-256(app_compose) = compose-hash event", 4.52, 3.08, 5.82, .28,
         13, PURPLE)
    # Replay is accepted only against the RTMR3 in an authenticated quote.
    route([(4.26, 4.39), (4.26, 4.86)], PURPLE)
    text("Replayed RTMR3 = authenticated quote RTMR3", 4.52, 4.48, 5.82, .28,
         13, PURPLE)

    # Conjunction of checks, not three alternative admission paths.
    for y in [2.525, 3.925, 5.425]:
        route([(10.51, y), (10.82, y)], PURPLE, False)
    route([(10.82, 2.525), (10.82, 5.425)], PURPLE, False)
    route([(10.82, 3.925), (11.10, 3.925)], GREEN)
    b.add_oval(slide, 11.45, 3.02, .66, .66, TINT[GREEN], GREEN, 1.2)
    route([(11.60, 3.34), (11.73, 3.47), (11.99, 3.20)], GREEN, False, 2.4)
    text("Verified\nworker", 11.12, 3.81, 1.34, .66, 18, GREEN, True)
    text("All checks\npass", 11.12, 4.61, 1.34, .52, 13, MUTED)

    b.add_note(slide, """The previous slide provisions the expected worker-image Digest in DeviceRegistry. This slide explains how the independently supplied live evidence is checked against that policy.

The worker obtains exact measured app_compose bytes, an ordered RTMR3 event log and a TDX Quote V4 from dstack. It performs preliminary consistency checks and submits all three in a single DeviceRegistry.registerDeviceWithAttestedAppCompose transaction, signed by its TEE action authority. The quote is supplied alongside the log; replay does not create the quote. The arrows are evidence dependencies, not an instruction to execute the Solidity functions in this visual order.

Everything inside the purple boundary is checked on chain. DeviceRegistry derives the pinned image Digest, SHA-256 of the exact app_compose bytes, and the normalized worker-policy hash. It compares the Digest with expectedWorkerImageDigest and requires an allowed worker policy. The state field contains the 32-byte Registry image digest extracted from the CI-provisioned immutable reference. The event log contains a compose-hash event, not the image Digest itself.

DeviceRegistry calls AutomataDcapTdxV4Attestation, the DCAP verifier. It authenticates the TDX quote through the Intel-rooted PCK certificate chain and quote/QE signatures, collateral and TCB appraisal, and checks the expected MRTD and RTMR0–2 base-runtime measurements. The verifier requires exactly one compose-hash event matching SHA-256 of the exact app_compose preimage. It replays the ordered RTMR3 runtime events with SHA-384 from a 48-byte all-zero initial value, including event-type and event-digest checks, and compares the result with the RTMR3 authenticated in the quote body. App-compose hashing and RTMR3 extension use different hash functions.

DeviceRegistry also verifies enrollment authorization and REPORTDATA binding to the registration fields, including participant, action authority, RSA public key, receipt key where applicable, workload, endpoints and fresh nonce. Successful admission therefore requires the conjunction of quote authenticity, trusted base runtime, allowed image and workload policy, event-log binding/replay, and enrollment/key binding. The source image policy and trusted runtime remain trust assumptions; an authenticated image does not itself prove data quality or bug-free training.

Source map, local prototype checked 20 September 2026:
vita-fl/dfl/node_server/src/server.ts:977–1001,1844–1866
vita-fl/dfl/node_server/src/bc_client.ts:1146,1226
vita-fl/smart_contracts/src/core/DeviceRegistry.sol:308–344,428–434,487–503
vita-fl/smart_contracts/src/attestation/AppComposeImage.sol:831
vita-fl/smart_contracts/src/attestation/AutomataDcapTdxV4Attestation.sol:151–171,310,458–506
""")
    return slide


def keys(prs, b):
    slide = b.new_content_slide(
        prs, 15, "Application-bound keys with dstack",
        "Separate derivation paths for DFL actions, model-key custody and inference receipts",
    )
    text, panel, route = _drawing(b, slide)

    panel(.65, 1.65, 5.58, 1.10, GREEN)
    text("Attested dstack KMS", .88, 1.80, 5.12, .40, 22, GREEN, True)
    text("Authorize workload · protect application root", .88, 2.31, 5.12, .26,
         14)
    panel(7.10, 1.65, 5.58, 1.10, BLUE)
    text("GetKey(path) via dstack.sock", 7.33, 1.80, 5.12, .40, 21, BLUE, True)
    text("Application-bound material · distinct paths", 7.33, 2.31, 5.12, .26,
         14)
    route([(6.29, 2.20), (7.04, 2.20)], BLUE, True, 2)

    route([(9.89, 2.79), (9.89, 3.12)], BLUE, False)
    route([(2.495, 3.12), (10.835, 3.12)], BLUE, False)
    for center in [2.495, 6.665, 10.835]:
        route([(center, 3.12), (center, 3.39)], BLUE)

    for x, color, title in [(.65, BLUE, "Action signing"),
                             (4.82, PURPLE, "Model-key custody"),
                             (8.99, GREEN, "Receipt signing")]:
        panel(x, 3.43, 3.69, 2.13, color)
        text(title, x + .17, 3.65, 3.35, .33, 19, color, True)

    text("HMAC-SHA-256\nsecp256k1", .82, 4.17, 3.35, .61, 17, BLUE, True)
    text("Authorize DFL transactions", .82, 5.00, 3.35, .27, 14)
    text("HKDF → AES-256-GCM", 4.99, 4.24, 3.35, .34, 16, PURPLE, True)
    text("Seal / recover a\nrandom RSA-3072 key", 4.99, 4.88, 3.35, .53, 14)
    text("Ed25519", 9.16, 4.24, 3.35, .34, 20, GREEN, True)
    text("Sign inference receipts\nSeparate Sello and AIR paths", 9.16, 4.88,
         3.35, .53, 13.5)

    panel(.65, 5.82, 12.03, .42, BLUE, "F5F8FA")
    text("Same application root, path and context → same derived key",
         .88, 5.89, 11.57, .25, 14.5, BLUE, True)

    b.add_note(slide, """This slide expands the former key-derivation half into three distinct operational purposes. dstack KMS authorization and VITA-FL on-chain worker admission are separate checks. DeviceRegistry does not release the KMS secrets; the visual sequence of the two slides is explanatory, not a boot-order dependency.

The attested dstack KMS protects root material and authorizes the application under its workload policy. Within the guest, the application calls GetKey through /var/run/dstack.sock. The application root and requested derivation path scope the returned material. VITA-FL then applies purpose-specific derivation and context. Same image alone is insufficient to guarantee the same key: the application root/KMS context, path and additional derivation context must also remain stable. The optional GetKey purpose concerns signature-chain metadata; distinct paths separate key bytes. Returned material is available in workload memory and must be protected there.

ACTION SIGNING: vita-fl/participant-ethereum-action/v1 returns material used with HMAC-SHA-256 and participant, chain ID and DeviceRegistry address context to derive a valid secp256k1 scalar. The action authority signs authorized protocol transactions, is re-derived for signing, and is checked against the startup address. The action signer rejects value transfers.

MODEL-KEY CUSTODY: vita-fl/participant-rsa-wrap/v1 returns material from which HKDF-SHA-256 derives an AES-256-GCM wrapping key. The participant RSA-3072 key is generated randomly when sealed state does not exist; it is not deterministically derived from dstack. The AES key seals the PKCS#8 private key with participant identity as associated data. Existing sealed state is unsealed on restart. Stable RSA identity requires retaining that sealed state; re-deriving the wrapping key alone cannot recreate a lost random RSA key. The RSA key signs/decrypts model artifacts and allows the inference worker to decrypt the published model bundle. Persistent storage contains sealed state, while working PEM files reside in /run/vita-fl tmpfs.

RECEIPT SIGNING: The current Sello receiver uses vita-fl/sello/tee-inference/v1, with HMAC-SHA-256 and participant/chain/registry/service context producing an Ed25519 seed. The Python receiver independently derives the same signing identity. AIR evidence uses a separate master-thesis/air-v1 path and Ed25519 key. The two protocols do not share a single receipt key. Their detailed paths are left in notes so the slide can concentrate on the shared key-derivation principle.

The action authority, RSA public key and inference worker's Sello receipt public key are bound into quote REPORTDATA during DeviceRegistry enrollment, connecting these operational identities to the verified workload on the preceding slide. AIR binds its own receipt public key and manifest/request context in separate inference evidence. Private key bytes are not written into the registry.

Source map, local prototype checked 20 September 2026:
vita-fl/dfl/node_server/src/action_key.ts:10–11,65–101,185,217
vita-fl/dfl/node_server/src/participant_key.ts:14,81,164–178,247–279
vita-fl/dfl/node_server/src/sello_key.ts:5,61,92
vita-fl/agent_receipts/dstack_key.py:32,91
vita-fl/tee_inference/service/attestation.py:56–71
vita-fl/dfl/node_server/src/server.ts:1834–1866,2893–2915
vita-fl/smart_contracts/src/core/DeviceRegistry.sol:342–344
vita-fl/phala/README.md:460,477–484
""")
    return slide

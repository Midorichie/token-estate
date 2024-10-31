;; token-estate.clar
(define-non-fungible-token property-token uint)

(define-data-var total-properties uint u0)

(define-map properties
    uint 
    {
        owner: principal,
        total-tokens: uint,
        available-tokens: uint,
        price-per-token: uint,
        property-hash: (buff 32)
    }
)

(define-map token-holdings
    { property-id: uint, holder: principal }
    uint
)

(define-constant contract-owner tx-sender)

;; Error constants
(define-constant err-not-authorized (err u100))
(define-constant err-invalid-property (err u101))
(define-constant err-insufficient-tokens (err u102))

;; Tokenize new property
(define-public (tokenize-property 
    (total-tokens uint) 
    (price-per-token uint)
    (property-hash (buff 32)))
    (let
        ((property-id (+ (var-get total-properties) u1)))
        (try! (nft-mint? property-token property-id tx-sender))
        (map-set properties property-id
            {
                owner: tx-sender,
                total-tokens: total-tokens,
                available-tokens: total-tokens,
                price-per-token: price-per-token,
                property-hash: property-hash
            }
        )
        (var-set total-properties property-id)
        (ok property-id)
    )
)

;; Purchase tokens
(define-public (purchase-tokens 
    (property-id uint)
    (token-amount uint))
    (let
        ((property (unwrap! (map-get? properties property-id) (err err-invalid-property)))
         (current-holdings (default-to u0 (map-get? token-holdings 
            { property-id: property-id, holder: tx-sender }))))
        
        (asserts! (<= token-amount (get available-tokens property)) err-insufficient-tokens)
        
        ;; Transfer payment
        (try! (stx-transfer? 
            (* token-amount (get price-per-token property))
            tx-sender
            (get owner property)))
        
        ;; Update holdings
        (map-set token-holdings
            { property-id: property-id, holder: tx-sender }
            (+ current-holdings token-amount))
        
        ;; Update available tokens
        (map-set properties property-id
            (merge property 
                { available-tokens: (- (get available-tokens property) token-amount) }))
        
        (ok true)
    )
)

;; Create secondary market trade
(define-public (create-trade
    (property-id uint)
    (token-amount uint)
    (price-per-token uint))
    (let
        ((current-holdings (default-to u0 (map-get? token-holdings 
            { property-id: property-id, holder: tx-sender }))))
        
        (asserts! (>= current-holdings token-amount) err-insufficient-tokens)
        
        ;; Create trade listing
        (ok true)
    )
)

;; Property metadata functions
(define-read-only (get-property-details (property-id uint))
    (map-get? properties property-id)
)

(define-read-only (get-token-balance 
    (property-id uint)
    (holder principal))
    (default-to u0 
        (map-get? token-holdings { property-id: property-id, holder: holder }))
)
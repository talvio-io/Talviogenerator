// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

/**
 * @title TalvioGenerator
 * @notice Talvio Generator — 10,000 Black Dot robots on BNB Chain.
 *         Mint starts CLOSED. Only the owner can open it (setMintOpen),
 *         set the metadata base URI, and withdraw funds.
 *         Rules: first 2 mints per wallet are free, then 0.002 BNB each,
 *         max 20 paid mints per wallet, 10,000 total supply.
 *         tokenURI = baseURI + zero-padded 5-digit id + ".json"
 *         (matches collection-10000/metadata/00001.json … 10000.json).
 */
contract TalvioGenerator is ERC721, Ownable {
    using Strings for uint256;

    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant FREE_PER_WALLET = 2;
    uint256 public constant PAID_MAX_PER_WALLET = 20;
    uint256 public constant PAID_PRICE = 0.002 ether;

    uint256 public totalMinted;
    bool public mintOpen;
    string private _baseTokenURI;

    mapping(address => uint256) public freeClaimedOf;
    mapping(address => uint256) public paidMintedOf;

    event MintOpenChanged(bool open);
    event BaseURISet(string baseURI);

    constructor() ERC721("Talvio Generator", "TALVIO") Ownable(msg.sender) {}

    // ---------- Mint ----------
    function mint(uint256 qty) external payable {
        require(mintOpen, "Mint is not open yet");
        require(qty > 0, "Quantity must be at least 1");
        require(totalMinted + qty <= MAX_SUPPLY, "Exceeds max supply");

        uint256 freeLeft = FREE_PER_WALLET - freeClaimedOf[msg.sender];
        uint256 freeUsed = qty < freeLeft ? qty : freeLeft;
        uint256 paidQty = qty - freeUsed;

        require(
            paidMintedOf[msg.sender] + paidQty <= PAID_MAX_PER_WALLET,
            "Exceeds paid mint limit per wallet"
        );
        require(msg.value >= paidQty * PAID_PRICE, "Insufficient BNB sent");

        freeClaimedOf[msg.sender] += freeUsed;
        paidMintedOf[msg.sender] += paidQty;

        for (uint256 i = 0; i < qty; i++) {
            totalMinted += 1;
            _safeMint(msg.sender, totalMinted);
        }
    }

    /// @notice BNB cost for `wallet` to mint `qty` right now (free allowance applied).
    function costFor(address wallet, uint256 qty) external view returns (uint256) {
        uint256 freeLeft = FREE_PER_WALLET - freeClaimedOf[wallet];
        uint256 paidQty = qty > freeLeft ? qty - freeLeft : 0;
        return paidQty * PAID_PRICE;
    }

    // ---------- Owner controls (each one is an owner-signed transaction) ----------
    function setMintOpen(bool open_) external onlyOwner {
        mintOpen = open_;
        emit MintOpenChanged(open_);
    }

    function setBaseURI(string calldata uri) external onlyOwner {
        _baseTokenURI = uri;
        emit BaseURISet(uri);
    }

    function baseURI() external view returns (string memory) {
        return _baseTokenURI;
    }

    function withdraw() external onlyOwner {
        (bool ok, ) = payable(owner()).call{value: address(this).balance}("");
        require(ok, "Withdraw failed");
    }

    // ---------- Metadata ----------
    function _pad5(uint256 id) internal pure returns (string memory) {
        string memory s = id.toString();
        bytes memory b = bytes(s);
        if (b.length >= 5) return s;
        bytes memory out = new bytes(5);
        uint256 pad = 5 - b.length;
        for (uint256 i = 0; i < 5; i++) {
            out[i] = i < pad ? bytes1("0") : b[i - pad];
        }
        return string(out);
    }

    function tokenURI(uint256 id) public view override returns (string memory) {
        _requireOwned(id);
        if (bytes(_baseTokenURI).length == 0) return "";
        return string(abi.encodePacked(_baseTokenURI, _pad5(id), ".json"));
    }
}

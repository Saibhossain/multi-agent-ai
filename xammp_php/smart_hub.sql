-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Aug 14, 2025 at 12:53 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_hub`
--

-- --------------------------------------------------------

--
-- Table structure for table `ai_logs`
--

CREATE TABLE `ai_logs` (
  `id` int(11) NOT NULL,
  `direction` enum('user','assistant') NOT NULL,
  `content` text NOT NULL,
  `meta` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`meta`)),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int(11) NOT NULL,
  `name` varchar(120) NOT NULL,
  `email` varchar(180) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `faq`
--

CREATE TABLE `faq` (
  `id` int(11) NOT NULL,
  `question` varchar(255) NOT NULL,
  `answer` text NOT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `faq`
--

INSERT INTO `faq` (`id`, `question`, `answer`, `tags`, `created_at`) VALUES
(1, 'What are your business hours?', 'We are open 9am–6pm (GMT+6), Sunday–Thursday.', 'general,hours', '2025-08-14 08:49:51'),
(2, 'How do I track my order?', 'Provide your order number and we will check the status in our system.', 'orders,tracking', '2025-08-14 08:49:51'),
(3, 'What payment methods do you accept?', 'We accept Visa, Mastercard, American Express, bKash, Nagad, and bank transfers. Cryptocurrency payments coming soon!', 'payments,orders', '2025-08-14 10:24:57'),
(4, 'Do you offer international shipping?', 'Yes! We ship worldwide via DHL and FedEx. Delivery times vary by location (3-5 business days regionally, 7-14 days internationally).', 'shipping,international', '2025-08-14 10:24:57'),
(5, 'How can I reset my password?', 'Click \"Forgot Password\" on the login page, enter your email, and follow the instructions in the reset link (valid for 2 hours).', 'account,security', '2025-08-14 10:24:57'),
(6, 'What\'s your return policy?', '30-day return window for unused items with original packaging. Electronics have a 15-day return policy. Contact support for RMA first.', 'returns,refunds', '2025-08-14 10:24:57'),
(7, 'Are your products eco-friendly?', 'All our packaging is 100% biodegradable, and 70% of products use recycled materials. Look for the green leaf icon!', 'sustainability,products', '2025-08-14 10:24:57'),
(8, 'Can I modify my order after placing it?', 'Order modifications are possible within 1 hour of placement. Contact support immediately with your order number.', 'orders,changes', '2025-08-14 10:24:57'),
(9, 'Do you have bulk discounts?', 'Yes! 5-10 units: 5% off, 11-25 units: 10% off, 25+ units: Contact our sales team for custom pricing.', 'wholesale,discounts', '2025-08-14 10:24:57'),
(10, 'How do I contact customer support?', '24/7 support via: Live Chat (website), WhatsApp (+8801712345678), or email support@company.com. Response time <30 mins.', 'contact,support', '2025-08-14 10:24:57'),
(11, 'Where are your products manufactured?', 'Designed in California, manufactured in our Dhaka EPZ facility (ISO 9001 certified).', 'about,quality', '2025-08-14 10:24:57'),
(12, 'Why was my payment declined?', 'Common reasons: insufficient funds, bank fraud protection, or incorrect CVV. Try another card or contact your bank.', 'payments,troubleshooting', '2025-08-14 10:24:57'),
(13, 'What\'s the difference between Pro and Basic versions?', 'Pro includes API access, priority support, and advanced analytics. See comparison table on our pricing page.', 'products,comparison', '2025-08-14 10:24:57'),
(14, 'How do I apply a discount code?', 'Enter the code at checkout before payment. Multiple codes cannot be combined unless stated otherwise.', 'orders,discounts', '2025-08-14 10:24:57'),
(15, 'Is my data secure with you?', 'We use AES-256 encryption, regular pentests, and are GDPR compliant. Read our Security White Paper for details.', 'security,privacy', '2025-08-14 10:24:57'),
(16, 'Do you offer installation services?', 'Yes! Professional installation available for 15% of product cost. Schedule during checkout or after delivery.', 'services,installation', '2025-08-14 10:24:57'),
(17, 'What\'s your warranty policy?', '1-year limited warranty covering manufacturing defects. Extended warranties available for purchase.', 'warranty,support', '2025-08-14 10:24:57'),
(18, 'How do I cancel my subscription?', 'Go to Account > Subscriptions > Cancel. Pro-rated refunds available if canceled within 7 days of renewal.', 'billing,subscriptions', '2025-08-14 10:24:57'),
(19, 'Can I visit your showroom?', 'Our Dhaka showroom at Gulshan-2 is open 10am-8pm daily. Book appointments for product demos.', 'locations,visit', '2025-08-14 10:24:57'),
(20, 'Why hasn\'t my order shipped yet?', 'Most orders ship within 24hrs. Delays may occur during holidays or for custom items. Check your order status page.', 'orders,shipping', '2025-08-14 10:24:57'),
(21, 'How do I become a reseller?', 'Apply through our Partner Portal. Requirements: Business license and minimum $5k initial order.', 'wholesale,partnerships', '2025-08-14 10:24:57'),
(22, 'What languages do you support?', 'Our platform supports English, Bengali, Hindi, and Arabic. Customer service available in all four languages.', 'languages,support', '2025-08-14 10:24:57');

-- --------------------------------------------------------

--
-- Table structure for table `tickets`
--

CREATE TABLE `tickets` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `subject` varchar(200) NOT NULL,
  `status` enum('open','pending','closed') DEFAULT 'open',
  `priority` enum('low','normal','high') DEFAULT 'normal',
  `details` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `uploads`
--

CREATE TABLE `uploads` (
  `id` int(11) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `path` varchar(512) NOT NULL,
  `mime` varchar(120) DEFAULT NULL,
  `kind` enum('csv','pdf','other') DEFAULT 'other',
  `summary` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ai_logs`
--
ALTER TABLE `ai_logs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `faq`
--
ALTER TABLE `faq`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `uploads`
--
ALTER TABLE `uploads`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ai_logs`
--
ALTER TABLE `ai_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `faq`
--
ALTER TABLE `faq`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `tickets`
--
ALTER TABLE `tickets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `uploads`
--
ALTER TABLE `uploads`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tickets`
--
ALTER TABLE `tickets`
  ADD CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 20, 2026 at 07:35 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `adindiahub_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `campaigns`
--

CREATE TABLE `campaigns` (
  `campaign_id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `budget` decimal(10,2) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `campaign_name` varchar(255) DEFAULT NULL,
  `platform` varchar(100) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Active',
  `ad_video` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `campaigns`
--

INSERT INTO `campaigns` (`campaign_id`, `client_id`, `budget`, `start_date`, `end_date`, `campaign_name`, `platform`, `status`, `ad_video`) VALUES
(53, 43, 7000000.00, '2026-10-29', '2026-12-14', 'Tata Sierra EV-Green Diwali Offer', 'Instagram Ads', 'Active', 'Tata_Sierra_EV.mp4'),
(54, 43, 200000.00, '2026-03-15', '2026-03-17', 'MRF', 'Facebook Ads', 'Active', 'Tata_Sierra_EV.mp4');

-- --------------------------------------------------------

--
-- Table structure for table `campaign_requests`
--

CREATE TABLE `campaign_requests` (
  `request_id` int(11) NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `campaign_name` varchar(100) DEFAULT NULL,
  `platform` varchar(50) DEFAULT NULL,
  `budget` int(11) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `message` text DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `assigned_video` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `campaign_requests`
--

INSERT INTO `campaign_requests` (`request_id`, `client_id`, `campaign_name`, `platform`, `budget`, `start_date`, `end_date`, `message`, `status`, `created_at`, `assigned_video`) VALUES
(27, 43, 'Tata Sierra EV-Green Diwali Offer', 'Instagram Ads', 7000000, '2026-10-29', '2026-12-14', '', 'Assigned', '2026-02-16 07:19:05', NULL),
(28, 44, 'Smartwatch x launch', 'YouTube Ads', 600000, '2026-04-18', '2026-06-20', '', 'Approved', '2026-02-16 08:35:31', NULL),
(29, 45, 'Holiday Travel Deals – Explore  North East India', 'YouTube Ads', 50000, '2026-07-01', '2026-07-31', 'I want to make a Northeast India explore video for advertising and upload it on Youtube platform', 'Approved', '2026-02-19 08:24:12', NULL),
(30, 46, 'UPSC 2026 Crash Course', 'Facebook Ads', 50000, '2026-04-18', '2026-05-30', 'Show the features of the course in this video highlight the 50 % offers week in Marathi . motivation students.', 'Pending', '2026-02-19 09:16:04', NULL),
(31, 47, 'Jaguar-x-series the return of royalty', 'YouTube Ads', 75000, '2026-12-01', '2026-12-31', 'Hello adindiahub team\r\nNeed a 60 second youtube 30 second reels video for Jaguar X series launch highlight V8 engine luxury interior,5- Septi features show three yrs free maintenance offer and 0% Ganeshotsav\r\nEMI target audience Mumbai Pune Bangalore (Age30 to 50 )draft required by 20 November thanks', 'Pending', '2026-02-19 09:33:33', NULL),
(32, 43, 'MRF', 'Facebook Ads', 200000, '2026-03-15', '2026-03-17', 'xyz', 'Assigned', '2026-03-18 09:40:43', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `clients`
--

CREATE TABLE `clients` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `password` varchar(30) DEFAULT NULL,
  `profile_photo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clients`
--

INSERT INTO `clients` (`id`, `name`, `email`, `phone`, `created_at`, `password`, `profile_photo`) VALUES
(43, 'Pratik Unnad', 'pratik@gmail.com', '9371240152', '2026-02-16 07:17:42', 'pratik@', 'pratik.png'),
(44, 'Akash Kusekar', 'akash@gmail.com', '7666961345', '2026-02-16 08:34:40', 'akash@', NULL),
(45, 'Prathmesh Bagale', 'prathmesh@gmail.com', '9666761660', '2026-02-19 07:47:55', 'prathmesh@', 'prath.jpeg'),
(46, 'Rajesh Patil', 'rajesh@gmail.com', '7696665050', '2026-02-19 08:25:42', 'rajesh@', NULL),
(47, 'Mahesh Patil', 'mahesh@gmail.com', '7666961350', '2026-02-19 09:19:03', 'Mahesh@', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `contact_messages`
--

CREATE TABLE `contact_messages` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact_messages`
--

INSERT INTO `contact_messages` (`id`, `name`, `email`, `message`, `created_at`) VALUES
(6, 'Rajesh Patil', 'rajesh@gmail.com', 'I am interested In running A social media Campaign for My business .Please provide Details about Pricing And process', '2026-03-18 06:14:47');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('admin','client') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `role`) VALUES
(1, 'Mahesh Patil', 'patilmahesh1586@gmail.com', 'Mahesh@123', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `video_feedback`
--

CREATE TABLE `video_feedback` (
  `id` int(11) NOT NULL,
  `campaign_id` int(11) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `stars` int(11) DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `video_feedback`
--

INSERT INTO `video_feedback` (`id`, `campaign_id`, `client_id`, `stars`, `comment`, `created_at`) VALUES
(3, 53, 43, 1, 'The advertisement campaign for Tata Sierra EV Green is very impressive and creative. The video quality is excellent and clearly highlights the eco-friendly features of the electric vehicle. The message is easy to understand and very attractive to the target audience. Overall, the campaign is effective and helps to promote the brand image positively.', '2026-02-18 14:52:15'),
(5, 53, 43, 5, 'Everything is good.', '2026-02-20 07:19:50'),
(6, 53, 43, 5, 'Great\r\n!', '2026-03-14 09:12:02');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `campaigns`
--
ALTER TABLE `campaigns`
  ADD PRIMARY KEY (`campaign_id`),
  ADD KEY `client_id` (`client_id`);

--
-- Indexes for table `campaign_requests`
--
ALTER TABLE `campaign_requests`
  ADD PRIMARY KEY (`request_id`);

--
-- Indexes for table `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `contact_messages`
--
ALTER TABLE `contact_messages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `video_feedback`
--
ALTER TABLE `video_feedback`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `campaigns`
--
ALTER TABLE `campaigns`
  MODIFY `campaign_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT for table `campaign_requests`
--
ALTER TABLE `campaign_requests`
  MODIFY `request_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `clients`
--
ALTER TABLE `clients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `contact_messages`
--
ALTER TABLE `contact_messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `video_feedback`
--
ALTER TABLE `video_feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `campaigns`
--
ALTER TABLE `campaigns`
  ADD CONSTRAINT `campaigns_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `clients` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

import qualified Data.HashSet as HashSet


readInput :: String -> IO (HashSet.HashSet Integer)
readInput s = do
    content <- readFile s
    return (HashSet.fromList (map read (lines content)))


solve :: HashSet.HashSet Integer -> Integer -> Integer -> [Integer]
solve s n t
    | t < 0 || n < 1               = []
    | n == 1 && HashSet.member t s = [t]
    | otherwise                    = [a * r | a <- HashSet.toList s, r <- solve s (n-1) (t-a)]


main :: IO ()
main = do
    h <- readInput "input.txt"
    print (head (solve h 2 2020))
    print (head (solve h 3 2020))
    return ()

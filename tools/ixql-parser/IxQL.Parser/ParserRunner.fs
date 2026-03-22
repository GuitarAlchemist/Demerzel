namespace IxQL.Parser

/// Runs FParsec parsers and converts results to F# Result type.
/// Avoids FParsec name conflicts (Success/Ok/Error shadow F# builtins in F# 10).
module ParserRunner =

    open FParsec

    let runParser (parser: Parser<'a, unit>) (input: string) : Result<'a, string> =
        // FParsec's Success/Failure DU cases shadow F# builtins.
        // Use FSharp.Reflection to extract the result safely.
        let result = run parser input
        let unionCase, fields =
            FSharp.Reflection.FSharpValue.GetUnionFields(result, result.GetType())
        if unionCase.Name = "Success" then
            Result.Ok (fields.[0] :?> 'a)
        else
            Result.Error (fields.[0] :?> string)
